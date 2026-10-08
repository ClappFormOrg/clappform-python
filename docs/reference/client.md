# Client

The `Clappform` client and its constructor. One instance is one
`(cluster, location, credentials)` binding; the API families (`cf.data`,
`cf.client`, `cf.auth`, `cf.notifier`) hang off it. See
[API families](api-families.md) for the generated per-RPC surface.

::: clappform.Clappform

::: clappform.ApiKey

::: clappform.Credentials

::: clappform.RetryPolicy
