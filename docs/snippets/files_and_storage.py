"""Runnable source for the "files, Excel & storage" guide snippets.

Covers getting data out of and into collections as files: CSV bytes, Excel
workbooks, Azure Blob / Fileshare, and SFTP. The storage logic takes the SDK
client as an argument, so the docs-test job drives it with small stand-ins; the
blocks that construct a real Azure or paramiko client need those packages and a
live endpoint, so they are the only ones that do not run here. The Excel blocks
need ``xlsxwriter`` and run wherever it is installed.
"""

from __future__ import annotations

import io
import logging
import os
import posixpath
import tempfile
import time
import zipfile
from collections.abc import Callable
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import pandas as pd

from clappform.testing import LocalMock

log = logging.getLogger("files_and_storage")


def build_mock() -> LocalMock:
    mock = LocalMock()
    mock.seed_collection_slug("rental_units", id="rental_units-id")
    mock.seed(
        "rental_units-id",
        [
            {"unit_id": "U-1", "municipality": "Utrecht", "rent": 812.0, "status": "let"},
            {"unit_id": "U-3", "municipality": "Zeist", "rent": 690.0, "status": "let"},
            {"unit_id": "U-4", "municipality": "Utrecht", "rent": 901.0, "status": "let"},
        ],
    )
    mock.seed_collection_slug("partner_units", id="partner_units-id")
    mock.seed("partner_units-id", [])
    return mock


# ---- CSV -------------------------------------------------------------------


def csv_payload(df: pd.DataFrame) -> bytes:
    # --8<-- [start:csv-bytes]
    payload = df.to_csv(index=False).encode("utf-8")
    # --8<-- [end:csv-bytes]
    return payload


# ---- Excel -----------------------------------------------------------------

# --8<-- [start:excel-sheet-names]
_FORBIDDEN = str.maketrans({c: "_" for c in "[]:*?/\\"})


def safe_sheet_name(name: object, taken: set[str]) -> str:
    """An Excel-safe, unique sheet name: at most 31 chars, no []:*?/\\."""
    clean = str(name).translate(_FORBIDDEN).strip()[:31] or "Sheet"
    base, i = clean, 1
    while clean in taken:
        suffix = f"_{i}"
        clean = base[: 31 - len(suffix)] + suffix
        i += 1
    taken.add(clean)
    return clean
# --8<-- [end:excel-sheet-names]


# --8<-- [start:excel-write]
def write_workbook(data: pd.DataFrame | dict[str, pd.DataFrame], dest: str) -> str:
    """Write one DataFrame, or a {sheet_name: DataFrame} map, to an .xlsx file."""
    sheets = {"Sheet1": data} if isinstance(data, pd.DataFrame) else data
    taken: set[str] = set()

    with pd.ExcelWriter(dest, engine="xlsxwriter") as writer:
        for name, frame in sheets.items():
            sheet = safe_sheet_name(name, taken)
            frame.to_excel(writer, sheet_name=sheet, index=False)
            worksheet = writer.sheets[sheet]
            worksheet.freeze_panes(1, 0)  # keep the header row in view
            for col, column in enumerate(frame.columns):
                longest = max([len(str(column)), *frame[column].astype(str).map(len)])
                worksheet.set_column(col, col, min(longest + 2, 60))
    return dest
# --8<-- [end:excel-write]


def temp_path(suffix: str = "") -> str:
    # --8<-- [start:temp-file]
    # A named temp file that outlives this block, so the next step can read it.
    fd, path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    # --8<-- [end:temp-file]
    return path


# ---- Azure Storage ---------------------------------------------------------


def azure_service(RESOURCE_URL: str) -> str:
    # --8<-- [start:azure-service]
    host = urlparse(RESOURCE_URL).netloc.lower()
    if ".blob." in host:
        service = "blob"
    elif ".file." in host:
        service = "file"
    else:
        raise ValueError(f"expected a *.blob.* or *.file.* host, got {host!r}")
    # --8<-- [end:azure-service]
    return service


def azure_connect(RESOURCE_URL: str, SAS_TOKEN: str) -> Any:  # pragma: no cover
    """Needs the Azure SDK and a live account, so the docs test doesn't call it."""
    # --8<-- [start:azure-connect]
    from azure.storage.blob import BlobClient
    from azure.storage.fileshare import ShareFileClient

    # The URL carries no credential; the SAS token is passed separately.
    credential = SAS_TOKEN.lstrip("?")
    if azure_service(RESOURCE_URL) == "blob":
        client = BlobClient.from_blob_url(RESOURCE_URL, credential=credential)
    else:
        client = ShareFileClient.from_file_url(RESOURCE_URL, credential=credential)
    # --8<-- [end:azure-connect]
    return client


def blob_upload(client: Any, local_path: str) -> None:
    # --8<-- [start:azure-upload]
    # Stream from disk: the SDK reads the file in blocks, never all at once.
    with open(local_path, "rb") as fh:
        client.upload_blob(fh, overwrite=True)  # Fileshare: client.upload_file(fh)
    # --8<-- [end:azure-upload]


def blob_download(client: Any) -> str:
    # --8<-- [start:azure-download]
    fd, local_path = tempfile.mkstemp()
    with os.fdopen(fd, "wb") as fh:
        client.download_blob().readinto(fh)  # Fileshare: client.download_file()
    # --8<-- [end:azure-download]
    return local_path


def blob_list(container: Any) -> list[str]:
    # --8<-- [start:azure-list]
    # container = ContainerClient.from_container_url(CONTAINER_URL, credential=credential)
    names = [blob.name for blob in container.list_blobs()]
    # --8<-- [end:azure-list]
    return names


# ---- SFTP ------------------------------------------------------------------

# --8<-- [start:retry]
def with_retry(
    connect: Callable[[], Any],
    attempts: int = 4,
    retry_on: tuple[type[BaseException], ...] = (OSError, EOFError),
) -> Any:
    """Call connect(), retrying: once at once, then after 1 s, 2 s, 4 s, ..."""
    for attempt in range(1, attempts + 1):
        try:
            return connect()
        except retry_on as exc:
            if attempt == attempts:
                raise
            delay = 0 if attempt == 1 else 2 ** (attempt - 2)
            log.warning("connect failed (%d/%d): %s; retry in %ss", attempt, attempts, exc, delay)
            time.sleep(delay)
    raise ValueError("attempts must be at least 1")
# --8<-- [end:retry]


def sftp_connect(SFTP_CONFIG: dict[str, Any]) -> Any:  # pragma: no cover
    """Needs paramiko and a live server, so the docs test doesn't call it."""
    # --8<-- [start:sftp-connect]
    import paramiko

    ssh = paramiko.SSHClient()
    # Verify the server against known_hosts; refuse an unknown host key.
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.RejectPolicy())

    with_retry(
        lambda: ssh.connect(
            SFTP_CONFIG["Host"],
            port=int(SFTP_CONFIG.get("Port", 22)),
            username=SFTP_CONFIG["Username"],
            password=SFTP_CONFIG["Password"],
            timeout=int(SFTP_CONFIG.get("Timeout", 30)),
        ),
        # Network errors are OSError and retry. A rejected password raises
        # paramiko.AuthenticationException, which isn't, so it fails at once.
        retry_on=(OSError, EOFError),
    )
    ssh.get_transport().set_keepalive(30)  # keep long transfers from idling out
    sftp = ssh.open_sftp()
    # ... transfer, then: ssh.close()
    # --8<-- [end:sftp-connect]
    return sftp


# --8<-- [start:sftp-makedirs]
def sftp_makedirs(sftp: Any, remote_dir: str) -> None:
    """mkdir -p over SFTP: create each missing segment of remote_dir."""
    current = ""
    for part in remote_dir.strip("/").split("/"):
        if not part:
            continue
        current = f"{current}/{part}"
        try:
            sftp.stat(current)
        except OSError:
            sftp.mkdir(current)
# --8<-- [end:sftp-makedirs]


def sftp_upload(sftp: Any, local_path: str, remote_path: str) -> None:
    # --8<-- [start:sftp-transfer]
    sftp_makedirs(sftp, posixpath.dirname(remote_path))
    sftp.put(local_path, remote_path)  # upload, streamed from disk

    fd, downloaded = tempfile.mkstemp()
    os.close(fd)
    sftp.get(remote_path, downloaded)  # download, streamed to disk
    # --8<-- [end:sftp-transfer]


# ---- Many files ------------------------------------------------------------

# --8<-- [start:batch]
def run_batch(
    names: list[str], op: Callable[[str], Any], on_error: str = "stop"
) -> dict[str, dict[str, Any]]:
    """Apply op to every name. 'stop' raises on the first failure; 'continue'
    carries on and reports each failure."""
    if on_error not in ("stop", "continue"):
        raise ValueError(f"on_error must be 'stop' or 'continue', got {on_error!r}")
    ok: dict[str, Any] = {}
    errors: dict[str, Any] = {}
    for name in names:
        try:
            ok[name] = op(name)
        except Exception as exc:
            if on_error == "stop":
                raise
            errors[name] = str(exc)
            log.error("%s failed: %s", name, exc)
    return {"ok": ok, "errors": errors}
# --8<-- [end:batch]


# ---- Stand-ins for the SDK clients -----------------------------------------


class _FakeBlob:
    def __init__(self) -> None:
        self.data = b""

    def upload_blob(self, fh: Any, overwrite: bool = False) -> None:
        self.data = fh.read()

    def download_blob(self) -> Any:
        data = self.data

        class _Stream:
            def readinto(self, fh: Any) -> None:
                fh.write(data)

        return _Stream()


class _FakeContainer:
    def list_blobs(self) -> list[Any]:
        return [type("Blob", (), {"name": n})() for n in ("a.csv", "b.csv")]


class _FakeSftp:
    def __init__(self) -> None:
        self.dirs = {"/"}
        self.files: dict[str, bytes] = {}

    def stat(self, path: str) -> None:
        if path not in self.dirs:
            raise FileNotFoundError(path)

    def mkdir(self, path: str) -> None:
        self.dirs.add(path)

    def put(self, local: str, remote: str) -> None:
        assert posixpath.dirname(remote) in self.dirs
        self.files[remote] = Path(local).read_bytes()

    def get(self, remote: str, local: str) -> None:
        Path(local).write_bytes(self.files[remote])


def run(transport: LocalMock) -> None:
    from clappform import Clappform

    df = pd.DataFrame({"unit_id": ["U-1", "U-2"], "rent": [812.0, 745.5]})
    assert csv_payload(df).startswith(b"unit_id,rent")

    assert azure_service("https://acct.blob.core.windows.net/c/x.csv") == "blob"
    assert azure_service("https://acct.file.core.windows.net/s/x.csv") == "file"

    # Blob round trip through disk.
    blob = _FakeBlob()
    src = temp_path(".csv")
    Path(src).write_bytes(csv_payload(df))
    blob_upload(blob, src)
    got = blob_download(blob)
    assert Path(got).read_bytes() == csv_payload(df)
    assert blob_list(_FakeContainer()) == ["a.csv", "b.csv"]

    # Retry: the first connect fails, the immediate retry succeeds.
    calls = iter([OSError("reset"), "session"])

    def flaky() -> Any:
        result = next(calls)
        if isinstance(result, Exception):
            raise result
        return result

    assert with_retry(flaky) == "session"

    # SFTP: nested remote directories are created before the upload.
    sftp = _FakeSftp()
    sftp_upload(sftp, src, "/inbox/2026-09/units.csv")
    assert {"/inbox", "/inbox/2026-09"} <= sftp.dirs

    # Batch: one missing file, reported under 'continue'.
    def fetch(name: str) -> str:
        if name == "missing.csv":
            raise FileNotFoundError(name)
        return f"/tmp/{name}"  # noqa: S108 - a returned label, nothing is written

    result = run_batch(["a.csv", "missing.csv"], fetch, on_error="continue")
    assert list(result["ok"]) == ["a.csv"] and list(result["errors"]) == ["missing.csv"]

    cf = Clappform(location="acme", cluster="prod", api_key="cf_live_...", transport=transport)
    with cf:
        local_path = got
        # --8<-- [start:ingest]
        # A downloaded file is a local path: read it with pandas, then upsert
        # on the business key so a re-run updates rows instead of duplicating.
        incoming = pd.read_csv(local_path)
        written = cf.data.collection("partner_units").upsert(incoming, on="unit_id")
        log.info("loaded %d rows from %s", written, local_path)
        # --8<-- [end:ingest]
        assert written == 2
    for path in (src, got):
        os.remove(path)


def run_excel(transport: LocalMock) -> None:
    """The Excel blocks and the end-to-end export; needs xlsxwriter."""
    from clappform import Clappform

    taken: set[str] = set()
    assert safe_sheet_name("Q1/Q2 results", taken) == "Q1_Q2 results"
    assert safe_sheet_name("Q1/Q2 results", taken) == "Q1_Q2 results_1"
    assert safe_sheet_name("x" * 40, taken) == "x" * 31

    blob = _FakeBlob()
    cf = Clappform(location="acme", cluster="prod", api_key="cf_live_...", transport=transport)
    with cf:
        client = blob
        # --8<-- [start:export-pipeline]
        # 1. Read and reduce server-side.
        units = cf.data.collection("rental_units").read(
            pipeline=[{"$match": {"status": "let"}}]
        )
        # 2. Shape the report in pandas.
        summary = units.groupby("municipality", as_index=False).agg(
            units=("unit_id", "count"), avg_rent=("rent", "mean")
        )
        # 3. Write the workbook to a temp file.
        fd, workbook = tempfile.mkstemp(suffix=".xlsx")
        os.close(fd)
        write_workbook({"Summary": summary, "Units": units.drop(columns="_id")}, workbook)
        # 4. Upload it, streamed from disk, then clean up.
        with open(workbook, "rb") as fh:
            client.upload_blob(fh, overwrite=True)
        os.remove(workbook)
        # --8<-- [end:export-pipeline]

    with zipfile.ZipFile(io.BytesIO(blob.data)) as xlsx:
        workbook_xml = xlsx.read("xl/workbook.xml").decode()
    assert 'name="Summary"' in workbook_xml and 'name="Units"' in workbook_xml


if __name__ == "__main__":
    run(build_mock())
    run_excel(build_mock())
