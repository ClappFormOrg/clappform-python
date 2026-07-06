"""Contract smoke test against a live staging cluster.

Fakes prove the client stack is internally consistent; they cannot catch
drift between the client and a real server (a field renamed server-side, an
RPC a cluster does not yet serve, an auth or location-header expectation that
changed). This test dials a real staging cluster to catch exactly that.

It is **skipped unless** ``CLAPPFORM_CONTRACT_SMOKE`` is set, because it needs
network access and real credentials, so it never runs in the normal unit-test
suite (local or PR CI). The intended home is the proto-sync workflow, which
runs after regenerating stubs from a new ``commons`` tag — the one moment
client/server drift can appear. Point it at staging with:

    CLAPPFORM_CONTRACT_SMOKE=1
    CLAPPFORM_SMOKE_LOCATION=<tenant subdomain>
    CLAPPFORM_SMOKE_API_KEY=<staging api key>
    CLAPPFORM_SMOKE_CLUSTER=<cluster extension>   # optional; DNS-discovered if unset

The assertions stay deliberately shallow — a real round-trip and clean
teardown — so the test flags drift without depending on any tenant's data.
"""

from __future__ import annotations

import os

import pytest

from clappform import Clappform, ClappformError

_SMOKE_ENABLED = os.environ.get("CLAPPFORM_CONTRACT_SMOKE")

pytestmark = pytest.mark.skipif(
    not _SMOKE_ENABLED,
    reason="contract smoke test runs only when CLAPPFORM_CONTRACT_SMOKE is set "
    "(proto-sync workflow); needs a live staging cluster and credentials",
)


def _require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        pytest.fail(
            f"contract smoke test needs {name}; set it alongside "
            "CLAPPFORM_CONTRACT_SMOKE in the proto-sync workflow"
        )
    return value


@pytest.fixture
def staging_client():
    location = _require("CLAPPFORM_SMOKE_LOCATION")
    api_key = _require("CLAPPFORM_SMOKE_API_KEY")
    cluster = os.environ.get("CLAPPFORM_SMOKE_CLUSTER")
    kwargs = {"api_key": api_key}
    if cluster is not None:
        kwargs["cluster"] = cluster
    client = Clappform(location, **kwargs)
    yield client
    client.close()


def test_staging_collections_listing_round_trips(staging_client) -> None:
    """List collections against staging: proves auth, location header, and the
    collection listing wire shape all still line up with the live server."""
    try:
        page = staging_client.client.collection.get_all(page=1, limit=1)
    except ClappformError as exc:  # surface a typed failure, not a raw grpc error
        pytest.fail(f"staging contract check failed: {exc}")
    # Shape, not contents: pagination must be populated regardless of tenant data.
    assert page.pagination.page >= 1
    assert page.pagination.pages >= 0


def test_staging_auth_key_listing_round_trips(staging_client) -> None:
    """List API keys against staging: extends drift detection to the authoriser
    family (a different host/service than the client API above), catching auth
    wire-shape drift the collection listing can't."""
    try:
        page = staging_client.auth.api_key.read_all(page=1, limit=1)
    except ClappformError as exc:
        pytest.fail(f"staging auth contract check failed: {exc}")
    assert page.pagination.page >= 1
    assert page.pagination.pages >= 0


def test_staging_notifier_health_round_trips(staging_client) -> None:
    """Health-check the notifier family against staging — a tenant-data-free
    round-trip that flags drift on a third API family (and its host)."""
    try:
        status = staging_client.notifier.health.health()
    except ClappformError as exc:
        pytest.fail(f"staging notifier contract check failed: {exc}")
    # Shape only: the service reports itself and a status enum value.
    assert status.service or status.status is not None
