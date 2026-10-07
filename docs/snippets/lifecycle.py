"""Runnable source for the client-lifecycle section of the concepts guide.

These blocks use the real gRPC transport, because closing it is what they
show. No call reaches the network: every call is made on a closed client, which
fails before a channel opens. The test stubs DNS discovery.
"""

from __future__ import annotations

import pytest


def nightly_sync(cf) -> None:
    """Stand-in for the reader's own job."""
    assert cf.location


def run() -> None:
    # --8<-- [start:close]
    from clappform import Clappform

    with Clappform(location="acme", api_key="cf_live_...") as cf:
        nightly_sync(cf)
    # leaving the block closed cf's connections

    # without a with block, close the client yourself
    cf = Clappform(location="acme", api_key="cf_live_...")
    try:
        nightly_sync(cf)
    finally:
        cf.close()
    # --8<-- [end:close]

    # --8<-- [start:closed]
    from clappform import ConfigurationError

    try:
        cf.data.collection("sales_orders").read()
    except ConfigurationError as exc:
        print(exc)  # client is closed
    # --8<-- [end:closed]
    with pytest.raises(ConfigurationError, match="client is closed"):
        cf.data.collection("sales_orders").read()

    # --8<-- [start:clones]
    with Clappform(location="acme", cluster="", api_key="cf_live_...") as cf:
        beta = cf.with_location("beta")  # shares cf's connections
        beta.close()                     # does nothing: cf owns them
        nightly_sync(beta)
    # cf is closed now, and so is every clone that shared its connections
    # --8<-- [end:clones]
    with pytest.raises(ConfigurationError, match="client is closed"):
        beta.data.collection("sales_orders").read()

    # --8<-- [start:rediscovered]
    cf = Clappform(location="acme", api_key="cf_live_...")  # cluster discovered
    # A location on another cluster gets its own connections; close them.
    with cf.with_location("noord-brabant") as other:
        nightly_sync(other)
    cf.close()
    # --8<-- [end:rediscovered]
    assert other.cluster == "prod-lts" and cf.cluster == ""


if __name__ == "__main__":
    run()
