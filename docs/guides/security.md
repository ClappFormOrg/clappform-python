# Security & credentials

API keys are the only credential this line ships, and everything is explicit:
the library reads no config files and no environment variables. That puts you in
control of where secrets come from; this page covers using that well.

## Keep keys out of source

The client never reads the environment for you, so *you* decide the source. Pull
the key from a secret store or environment at the call site and pass it in;
never hard-code it, never commit it:

```python
--8<-- "security.py:connect-env"
```

The key travels as `x-api-key` metadata on every call. `repr(cf)` names only
the credential type, an `ApiKey` prints as `ApiKey(***)`, and error messages do
not include it.

In an actionflow worker the location and key come from the worker; see
[Running in an actionflow](actionflow-scripts.md).

!!! danger "Never commit a key"
    A key in a notebook cell, a script literal, or a committed `.env` is a
    leaked credential. If one lands in git history, rotate it (below) and treat
    the old one as compromised.

## Scope keys to what they need

The credential rides on every call from a client, because the client *is* a
`(cluster, location, credential)` binding. Prefer a key scoped to one location
and the minimum permissions for the job over a broad key reused everywhere: the
blast radius of a leak is what the key can do. `generate_key()` takes a
`permissions=` list for that.

## Rotating a key

Manage keys through the authoriser API, `cf.auth.api_key`. Generate a
replacement, cut over to it, then delete the old one, so a leaked or ageing key
stops working. `generate_key()` returns the new `APIKey`, whose `api_key` field
is the secret; `iter_read_all()` lists the keys that exist; `delete_key(id=...)`
revokes one.

```python
--8<-- "security.py:rotate"
```

`expiration_date` is required in practice: the authoriser rejects a date in the
past, and an unset field is the Unix epoch. Give each job its **own** key so
you can rotate one without disrupting the rest.

## Transport security

Connections are TLS by default. The `insecure=True` escape hatch exists only for
local development against a plaintext endpoint, and sends the key unencrypted.
Never use it against a real cluster. Endpoint overrides (`endpoints=`) are for
reaching non-standard hosts, such as a local development server or a cluster
that moved port, not for disabling transport security. The default ports are
`:50051` for the main cluster and 443 for every other cluster; both use TLS.

See the [Client reference](../reference/client.md) for the constructor's
security-relevant arguments and the [Authoriser reference](../reference/api-auth.md)
for the full key-management surface.
