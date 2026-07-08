# Security & credentials

API keys are the only credential this line ships, and everything is explicit —
the library reads no config files and no environment variables. That puts you in
control of where secrets come from; this page covers using that well.

## Keep keys out of source

The client never reads the environment for you, so *you* decide the source. Pull
the key from a secret store / environment at the call site and pass it in —
never hard-code it, never commit it:

```python
import os

from clappform import Clappform

cf = Clappform(location="acme", api_key=os.environ["CLAPPFORM_API_KEY"])
```

In an actionflow worker the tenant and key come from the worker's environment;
see [Running inside an actionflow](actionflow-scripts.md).

!!! danger "Never commit a key"
    A key in a notebook cell, a script literal, or a committed `.env` is a
    leaked credential. If one lands in git history, rotate it (below) and treat
    the old one as compromised.

## Scope keys to what they need

The credential rides on every call from a client — the client *is* a
`(cluster, location, credential)` binding. Prefer a key scoped to one tenant and
the minimum permissions for the job over a broad key reused everywhere: the blast
radius of a leak is exactly what the key can do.

## Rotating a key

Manage keys through the authoriser API (`cf.auth.api_keys`). Generate a
replacement, cut over to it, then delete the old one — so a leaked or ageing key
stops working. `generate_key()` returns the new `APIKey`; `read_all()` lists what
exists.

```python
# Illustrative — talks to a live authoriser.
new_key = cf.auth.api_keys.generate_key(
    name="nightly-etl",
    expiration_date=EPOCH_SECONDS,      # set an expiry; don't mint eternal keys
)
# ... store new_key, redeploy jobs to use it, then revoke the old one.
```

Give keys an **expiry** so an unrotated key fails closed rather than living
forever, and give each job its **own** key so you can rotate one without
disrupting the rest.

## Transport security

Connections are TLS by default. The `insecure=True` escape hatch exists only for
local development against a plaintext endpoint — never use it against a real
cluster. Endpoint overrides (`endpoints=`) are for reaching non-standard hosts
(e.g. a legacy `:50051` cluster), not for disabling transport security.

See the [Client reference](../reference/client.md) for the constructor's
security-relevant arguments and the [authoriser reference](../reference/api-families.md)
for the full key-management surface.
