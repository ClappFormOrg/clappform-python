"""Runnable source for the security & credentials guide snippets.

The key-rotation block talks to the authoriser API; here its three RPCs are
stubbed on ``LocalMock`` so the block runs in CI.
"""

from __future__ import annotations

from clappform.testing import LocalMock


def build_mock() -> LocalMock:
    from clappform.gen.clappform.authoriser.v1.apikey import apikey_pb2
    from clappform.gen.clappform.v1.commons import commons_pb2

    mock = LocalMock()
    keys = [apikey_pb2.APIKey(id="key-old", name="nightly-etl-2026q2")]

    def _generate(request):
        key = apikey_pb2.APIKey(
            id="key-new",
            name=request.name,
            api_key="cf_live_new_secret",
            expiration_date=str(request.expiration_date),
        )
        keys.append(key)
        return key

    def _read_all(_request):
        return apikey_pb2.APIKeys(
            api_keys=keys, pagination=commons_pb2.Pagination(page=1, pages=1, total=len(keys))
        )

    def _delete(request):
        keys[:] = [key for key in keys if key.id != request.id]
        return commons_pb2.Message(message="deleted")

    mock.on("/clappform.authoriser.v1.apikey.APIKeyManagement/GenerateKey", _generate)
    mock.on("/clappform.authoriser.v1.apikey.APIKeyManagement/ReadAll", _read_all)
    mock.on("/clappform.authoriser.v1.apikey.APIKeyManagement/DeleteKey", _delete)
    return mock


def store_secret(name: str, value: str) -> None:
    """Stand-in for writing to the reader's secret store."""
    assert name and value


def run(transport: LocalMock) -> None:
    # --8<-- [start:connect-env]
    import os

    from clappform import Clappform

    cf = Clappform(location="acme", api_key=os.environ["CLAPPFORM_API_KEY"])
    # --8<-- [end:connect-env]
    cf.close()

    cf = Clappform(location="acme", api_key="cf_live_...", transport=transport)

    with cf:
        # --8<-- [start:rotate]
        from datetime import datetime, timedelta, timezone

        # 1. Mint the replacement. expiration_date is Unix seconds and must be
        #    in the future; the authoriser rejects a date in the past.
        expires = datetime.now(timezone.utc) + timedelta(days=90)
        new_key = cf.auth.api_key.generate_key(
            name="nightly-etl-2026q3",
            expiration_date=int(expires.timestamp()),
        )

        # 2. Store new_key.api_key, the secret, and redeploy the jobs that use
        #    the old key.
        store_secret("CLAPPFORM_API_KEY", new_key.api_key)

        # 3. Revoke the old key by its id, so a leaked copy stops working.
        old = next(k for k in cf.auth.api_key.iter_read_all() if k.name == "nightly-etl-2026q2")
        cf.auth.api_key.delete_key(id=old.id)
        # --8<-- [end:rotate]

        remaining = [key.name for key in cf.auth.api_key.iter_read_all()]
        assert remaining == ["nightly-etl-2026q3"]


if __name__ == "__main__":
    run(build_mock())
