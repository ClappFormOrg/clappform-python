# Files, Excel & storage

A lot of work with a collection starts or ends with a file: a CSV a partner
drops on an SFTP server, a monthly Excel report, an export pushed to Azure
Storage. The client itself only speaks DataFrames; this guide covers the step
between a DataFrame and a file, and moving that file.

The code runs in CI. The storage functions take the Azure or SFTP client as an
argument, and the tests drive them with stand-ins; only the blocks marked
**needs a live endpoint** go untested, because they construct a real client.

## Two rules for files

**Pass paths, not bytes.** Write a file to disk, and hand the next step its
path. The Azure and SFTP SDKs stream from and to a file in blocks, so a large
file never sits whole in memory. In an actionflow, output the path from one
task and read it in the next.

**Use a temp file when nobody needs the name.** `mkstemp` creates a file that
survives until you remove it, unlike `NamedTemporaryFile`, which deletes it when
it closes:

```python
--8<-- "files_and_storage.py:temp-file"
```

## DataFrame to CSV

For an upload, CSV bytes without the index:

```python
--8<-- "files_and_storage.py:csv-bytes"
```

Drop the index unless it carries data. A DataFrame from `read()` has a plain
range index, which becomes an unnamed first column in the file.

## DataFrame to Excel

`to_excel` needs an engine: `xlsxwriter` to write, `openpyxl` to read an `.xlsx`
back with `read_excel`. Install whichever you use; neither ships with this
client.

### Safe sheet names

Excel caps a sheet name at 31 characters and forbids `[ ] : * ? / \`. A name
built from data (`"Q1/Q2 results"`, a municipality, a long product name) needs
cleaning, and two names can collide once cleaned:

```python
--8<-- "files_and_storage.py:excel-sheet-names"
```

`"Q1/Q2 results"` becomes `Q1_Q2 results`, and a second one `Q1_Q2 results_1`.

### One workbook, one or more sheets

Take a DataFrame, or a `{sheet_name: DataFrame}` map for several sheets. The
header row stays frozen while scrolling, and each column is sized to its widest
value, capped at 60 characters:

```python
--8<-- "files_and_storage.py:excel-write"
```

Keep report-specific formatting (number formats, colours, charts) out of a
shared helper like this. It belongs next to the report that needs it.

## Azure Storage

`azure-storage-blob` and `azure-storage-file-share` are separate packages from
this client. One URL shape covers both services; the host tells them apart:

```python
--8<-- "files_and_storage.py:azure-service"
```

### Connect with a SAS token

Keep the SAS token out of the URL. The URL is safe to log and to show in a task
configuration; the token is a credential, and belongs in a secret. Pass it as
`credential=`:

```python
--8<-- "files_and_storage.py:azure-connect"
```

*Needs a live endpoint.* `lstrip("?")` accepts a token stored with or without
its leading `?`.

### Upload, download, list

```python
--8<-- "files_and_storage.py:azure-upload"
```

```python
--8<-- "files_and_storage.py:azure-download"
```

```python
--8<-- "files_and_storage.py:azure-list"
```

A Fileshare client has the same shape with different names: `upload_file`,
`download_file`, `delete_file`, and `ShareDirectoryClient.list_directories_and_files()`
for a listing.

## SFTP

`paramiko` is the usual library. SFTP connects fail intermittently, so retry
the connect with a short backoff. Retry network errors only: a wrong password
fails the same way every time.

```python
--8<-- "files_and_storage.py:retry"
```

### Connect

```python
--8<-- "files_and_storage.py:sftp-connect"
```

*Needs a live endpoint.* This verifies the server's host key against
`known_hosts` and refuses an unknown one. `AutoAddPolicy` would accept any key
on first contact, which also accepts an attacker who answers in the server's
place. Add the server's key to `known_hosts` once, when you set the connection
up.

### Upload and download

SFTP has no `mkdir -p`, so create each missing directory before an upload into
a new path:

```python
--8<-- "files_and_storage.py:sftp-makedirs"
```

```python
--8<-- "files_and_storage.py:sftp-transfer"
```

`put` and `get` stream in blocks. Open one session for every file in a run,
rather than one per file.

## Many files in one run

When one step handles a list of files, decide what one failure means. `stop`
raises on the first failure, which suits files that only make sense together.
`continue` processes the rest and reports each failure, which suits a daily
batch where one missing file shouldn't block the others:

```python
--8<-- "files_and_storage.py:batch"
```

The result is `{"ok": {name: value}, "errors": {name: message}}`. Check
`errors` before a later step that must not run on partial input.

## A file into a collection

A downloaded file is a local path. Read it with pandas, then write the
DataFrame. `upsert` on the business key keeps a re-run from duplicating rows:

```python
--8<-- "files_and_storage.py:ingest"
```

pandas picks the reader from the format: `read_csv`, `read_excel`,
`read_parquet`, `read_json`. For more on the write side, see
[Load a file into a collection](cookbook.md#load-a-file-into-a-collection).

## End to end: collection to an Excel report in Azure

Read and filter server-side, shape the report in pandas, write the workbook to
a temp file, and upload it from disk:

```python
--8<-- "files_and_storage.py:export-pipeline"
```

`client` is the `BlobClient` from [Connect with a SAS token](#connect-with-a-sas-token).
To deliver over SFTP, swap step 4 for `sftp.put(workbook, remote_path)`.

As an actionflow, the same flow splits into tasks at the natural seams: a read
task outputs the DataFrame, a transform task outputs the summary, an export
task outputs `workbook` (the path), and an upload task takes that path. See
[Writing actionflow tasks](actionflow-scripts.md#handing-data-between-tasks).
