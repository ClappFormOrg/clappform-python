"""Runnable source for the troubleshooting / FAQ guide snippets.

Each block reproduces a real symptom and shows the fix. Runs against
``LocalMock`` in CI so the "do this instead" code is guaranteed to work.
"""

from __future__ import annotations

import pytest

from clappform.testing import LocalMock


def build_mock() -> LocalMock:
    mock = LocalMock()
    mock.seed_collection_slug("orders", id="orders-id")
    mock.seed(
        "orders-id",
        [
            {"status": "open", "amount": 10.0, "label": "A"},
            {"status": "open", "amount": 20.0, "label": "B"},
        ],
    )
    return mock


def run(transport: LocalMock) -> None:
    from clappform import Clappform, NotFoundError

    cf = Clappform(location="acme", cluster="prod", api_key="cf_live_...", transport=transport)

    with cf:
        col = cf.data.collection("orders")

        # --8<-- [start:consumed-result]
        # SYMPTOM: "this ReadResult has already been consumed". A result set
        # streams once. FIX: don't reuse a fetch(); take what you need in one
        # pass, or call fetch()/read() again for a fresh stream.
        from clappform import ClappformError

        result = col.fetch(pipeline=[{"$match": {"status": "open"}}])
        df = result.to_pandas()          # first pass consumes the stream
        with pytest.raises(ClappformError):
            list(result)                 # second pass on the SAME result: error
        again = col.read(pipeline=[{"$match": {"status": "open"}}])  # fresh pass
        # --8<-- [end:consumed-result]
        assert len(df) == 2 and len(again) == 2

        # --8<-- [start:not-found]
        # SYMPTOM: NotFoundError on a slug you're sure exists. Usually a typo,
        # wrong tenant, or the collection was recreated. FIX: branch on it; the
        # message names the slug and the location it searched.
        try:
            cf.data.collection("does-not-exist").read()
        except NotFoundError as exc:
            missing = str(exc)           # includes the slug + location
        # --8<-- [end:not-found]
        assert "does-not-exist" in missing

        # --8<-- [start:group-in-mock]
        # SYMPTOM: a $group pipeline returns the raw rows unchanged in a test.
        # CAUSE: LocalMock runs $match/$project/$limit but does NOT compute
        # $group (it's a transport double, not an aggregation engine). FIX: stub
        # the grouped answer with .on() for that pipeline.
        from clappform.gen.clappform.data.v1.aggregate import aggregate_pb2

        mock = build_mock()
        mock.on(
            "/clappform.data.v1.aggregate.AggregateManagement/AggregateStream",
            [aggregate_pb2.AggregateResponse(data=b'[{"_id":"A","n":1}]')],
        )
        with Clappform(location="acme", cluster="prod", api_key="x", transport=mock) as c2:
            grouped = c2.data.collection("orders").aggregate(
                [{"$group": {"_id": "$label", "n": {"$sum": 1}}}]
            )
        # --8<-- [end:group-in-mock]
        assert list(grouped["_id"]) == ["A"]

        # --8<-- [start:per-call-timeout]
        # SYMPTOM: a big read trips the default deadline (TransientError /
        # DEADLINE_EXCEEDED). FIX: raise the deadline for that one call with
        # timeout=, without changing the client-wide default.
        big = col.read(pipeline=[{"$match": {"status": "open"}}], timeout=120.0)
        # --8<-- [end:per-call-timeout]
        assert len(big) == 2


if __name__ == "__main__":
    run(build_mock())
