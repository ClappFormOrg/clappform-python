# API families

The four API families hang off the client: `cf.data`, `cf.client`, `cf.auth`,
and `cf.notifier`. Each is a generated sub-client with one method per RPC, and
these pages are generated from those wrappers' docstrings, which come from the
proto comments, so a new RPC appears here in the same release that adds it to
the client.

For the everyday DataFrame flows on `cf.data`, prefer the
[DataFrame surface](dataframes.md) (`cf.data.collection(...)` /
`cf.data.query(...)`); the raw per-RPC methods below are the full generated
surface underneath it.

## Data: `cf.data`

::: clappform.services.data
    options:
      show_root_heading: false
      show_root_toc_entry: false
      members_order: alphabetical
      filters: ["!^_", "!API$"]

## Client: `cf.client`

::: clappform.services.client
    options:
      show_root_heading: false
      show_root_toc_entry: false
      members_order: alphabetical
      filters: ["!^_", "!API$"]

## Authoriser: `cf.auth`

::: clappform.services.auth
    options:
      show_root_heading: false
      show_root_toc_entry: false
      members_order: alphabetical
      filters: ["!^_", "!API$"]

## Notifier: `cf.notifier`

::: clappform.services.notifier
    options:
      show_root_heading: false
      show_root_toc_entry: false
      members_order: alphabetical
      filters: ["!^_", "!API$"]
