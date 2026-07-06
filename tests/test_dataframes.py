"""Collection/query handles and ReadResult — the DataFrame surface.

Drives the flows through the real ``Clappform`` client against ``LocalMock``,
exactly as customers and ``examples/`` do: seed a collection, read it into a
frame, mutate, and write back, asserting the store reflects each flow.
"""

import pandas as pd
import pytest

from clappform import Clappform, ClappformError, ReadResult
from clappform.dataframes import CollectionHandle, QueryHandle
from clappform.testing import LocalMock

CID = "1c9a7f3e-0000-4000-8000-000000000001"


@pytest.fixture
def cf():
    mock = LocalMock()
    client = Clappform("acme", "qa", api_key="k", transport=mock)
    yield client, mock
    client.close()


def _seed_orders(mock):
    mock.seed(
        CID,
        [
            {"order_id": 1, "status": "open", "amount": 10.0},
            {"order_id": 2, "status": "closed", "amount": 20.0},
            {"order_id": 3, "status": "open", "amount": 30.0},
        ],
    )


# -- reads ---------------------------------------------------------------


def test_read_returns_whole_collection_as_frame(cf) -> None:
    client, mock = cf
    _seed_orders(mock)
    df = client.data.collection(CID).read()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert "_id" in df.columns  # kept for round-trip updates


def test_read_where_filters_rows(cf) -> None:
    client, mock = cf
    _seed_orders(mock)
    df = client.data.collection(CID).read(where={"status": "open"})
    assert sorted(df["order_id"]) == [1, 3]


def test_read_fields_projects_columns_but_keeps_id(cf) -> None:
    client, mock = cf
    _seed_orders(mock)
    df = client.data.collection(CID).read(fields=["order_id", "amount"])
    assert set(df.columns) == {"order_id", "amount", "_id"}


def test_read_limit_caps_rows(cf) -> None:
    client, mock = cf
    _seed_orders(mock)
    df = client.data.collection(CID).read(limit=2)
    assert len(df) == 2


def test_read_equals_fetch_to_pandas(cf) -> None:
    client, mock = cf
    _seed_orders(mock)
    col = client.data.collection(CID)
    from_read = col.read(where={"status": "open"})
    from_fetch = col.fetch(where={"status": "open"}).to_pandas()
    pd.testing.assert_frame_equal(from_read, from_fetch)


def test_fetch_returns_readresult(cf) -> None:
    client, mock = cf
    _seed_orders(mock)
    result = client.data.collection(CID).fetch()
    assert isinstance(result, ReadResult)
    assert len(list(result)) == 3


def test_readresult_is_single_pass(cf) -> None:
    client, mock = cf
    _seed_orders(mock)
    result = client.data.collection(CID).fetch()
    list(result)
    with pytest.raises(ClappformError, match="already been consumed"):
        list(result)


def test_iter_batches_yields_one_list_per_chunk(cf) -> None:
    client, mock = cf
    _seed_orders(mock)
    batches = list(client.data.collection(CID).iter_batches(batch_size=2))
    assert [len(b) for b in batches] == [2, 1]


def test_empty_collection_reads_empty_frame(cf) -> None:
    client, mock = cf
    mock.seed(CID, [])
    df = client.data.collection(CID).read()
    assert df.empty


def test_fetch_rejects_pipeline_with_sugar(cf) -> None:
    client, _mock = cf
    with pytest.raises(ValueError, match="not both"):
        client.data.collection(CID).fetch(pipeline=[{"$match": {}}], where={"x": 1})


def test_negative_limit_rejected(cf) -> None:
    client, _mock = cf
    with pytest.raises(ValueError, match="non-negative"):
        client.data.collection(CID).read(limit=-1)


def test_aggregate_passes_pipeline_through(cf) -> None:
    client, mock = cf
    _seed_orders(mock)
    # A $match stage the sugar could also emit — proves the custom path streams.
    df = client.data.collection(CID).aggregate([{"$match": {"status": "closed"}}])
    assert list(df["order_id"]) == [2]


# -- writes --------------------------------------------------------------


def test_append_inserts_rows_and_returns_count(cf) -> None:
    client, mock = cf
    mock.seed(CID, [])
    n = client.data.collection(CID).append(
        pd.DataFrame([{"order_id": 10}, {"order_id": 11}])
    )
    assert n == 2
    assert len(mock.records(CID)) == 2


def test_append_reports_progress_per_chunk(cf) -> None:
    client, mock = cf
    mock.seed(CID, [])
    seen: list[int] = []
    client.data.collection(CID).append(
        pd.DataFrame([{"n": i} for i in range(5)]),
        chunk_rows=2,
        progress=seen.append,
    )
    assert seen == [2, 4, 5]  # cumulative row count after each chunk


def test_append_empty_frame_writes_nothing(cf) -> None:
    client, mock = cf
    mock.seed(CID, [])
    n = client.data.collection(CID).append(pd.DataFrame())
    assert n == 0
    assert mock.records(CID) == []


def test_read_mutate_update_round_trip(cf) -> None:
    client, mock = cf
    _seed_orders(mock)
    col = client.data.collection(CID)
    df = col.read()
    df.loc[df["order_id"] == 1, "status"] = "archived"
    updated = col.update(df)  # defaults to on="_id", kept by read()
    assert updated == 3
    by_id = {r["order_id"]: r["status"] for r in mock.records(CID)}
    assert by_id[1] == "archived" and by_id[2] == "closed"


def test_update_missing_key_raises(cf) -> None:
    client, mock = cf
    _seed_orders(mock)
    with pytest.raises(ValueError, match="missing that column"):
        client.data.collection(CID).update(pd.DataFrame([{"status": "x"}]), on="_id")


def test_upsert_updates_existing_and_inserts_new(cf) -> None:
    client, mock = cf
    _seed_orders(mock)
    n = client.data.collection(CID).upsert(
        pd.DataFrame(
            [{"order_id": 2, "status": "reopened"}, {"order_id": 99, "status": "new"}]
        ),
        on="order_id",
    )
    assert n == 2
    by_id = {r["order_id"]: r["status"] for r in mock.records(CID)}
    assert by_id[2] == "reopened"
    assert by_id[99] == "new"
    assert len(mock.records(CID)) == 4


def test_replace_where_sets_values_on_matches(cf) -> None:
    client, mock = cf
    _seed_orders(mock)
    client.data.collection(CID).replace_where({"status": "open"}, {"status": "seen"})
    statuses = sorted(r["status"] for r in mock.records(CID))
    assert statuses == ["closed", "seen", "seen"]


def test_delete_by_where_removes_matches(cf) -> None:
    client, mock = cf
    _seed_orders(mock)
    client.data.collection(CID).delete(where={"status": "open"})
    assert [r["order_id"] for r in mock.records(CID)] == [2]


def test_delete_by_oids_removes_those_rows(cf) -> None:
    client, mock = cf
    mock.seed(CID, [{"_id": "a"}, {"_id": "b"}, {"_id": "c"}])
    client.data.collection(CID).delete(oids=["a", "c"])
    assert [r["_id"] for r in mock.records(CID)] == ["b"]


def test_delete_requires_exactly_one_selector(cf) -> None:
    client, _mock = cf
    col = client.data.collection(CID)
    with pytest.raises(ValueError, match="exactly one"):
        col.delete()
    with pytest.raises(ValueError, match="exactly one"):
        col.delete(where={"x": 1}, oids=["a"])


def test_delete_with_empty_where_is_refused_and_leaves_data(cf) -> None:
    # An empty filter matches everything; deleting the whole collection must be
    # explicit via clear(), never a side effect of an empty where=.
    client, mock = cf
    _seed_orders(mock)
    col = client.data.collection(CID)
    with pytest.raises(ValueError, match="use clear"):
        col.delete(where={})
    assert len(mock.records(CID)) == 3  # nothing was deleted


def test_clear_empties_collection(cf) -> None:
    client, mock = cf
    _seed_orders(mock)
    client.data.collection(CID).clear()
    assert mock.records(CID) == []


# -- pandas optional-dependency seam -------------------------------------


def test_to_pandas_without_pandas_raises_install_hint(cf, monkeypatch) -> None:
    client, mock = cf
    _seed_orders(mock)
    result = client.data.collection(CID).fetch()

    import builtins

    real_import = builtins.__import__

    def _no_pandas(name, *args, **kwargs):
        if name == "pandas":
            raise ImportError("no pandas")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", _no_pandas)
    with pytest.raises(ClappformError, match=r"pip install clappform\[pandas\]"):
        result.to_pandas()


# -- pipeline compilation -------------------------------------------------


def test_compiled_pipeline_matches_manual_aggregate(cf) -> None:
    """read(where/fields/limit) must send the same pipeline aggregate() would."""
    client, mock = cf
    _seed_orders(mock)
    col = client.data.collection(CID)

    col.read(where={"status": "open"}, fields=["order_id"], limit=1)
    sugar_pipeline = _last_pipeline(mock)

    col.aggregate(
        [
            {"$match": {"status": "open"}},
            {"$project": {"order_id": 1}},
            {"$limit": 1},
        ]
    )
    manual_pipeline = _last_pipeline(mock)
    assert sugar_pipeline == manual_pipeline


def _last_pipeline(mock: LocalMock):
    import json

    for call in reversed(mock.calls):
        if call.method.endswith("/AggregateStream"):
            return json.loads(call.request.pipeline)
    raise AssertionError("no AggregateStream call recorded")


def test_collection_handle_repr(cf) -> None:
    client, _mock = cf
    assert "CollectionHandle" in repr(client.data.collection(CID))
    assert isinstance(client.data.collection(CID), CollectionHandle)
    assert isinstance(client.data.query(CID), QueryHandle)


QID = "8f14e45f-ceea-467f-a34e-95b7f7f7a9d1"


def test_query_handle_fetch_returns_readresult(cf) -> None:
    client, mock = cf
    _seed_orders(mock)
    mock.seed_query(QID, collection=CID, id=QID)
    result = client.data.query(QID).fetch()
    assert isinstance(result, ReadResult)
    assert len(list(result)) == 3


def test_query_handle_iter_batches_streams_per_chunk(cf) -> None:
    client, mock = cf
    _seed_orders(mock)
    mock.seed_query(QID, collection=CID, id=QID)
    batches = list(client.data.query(QID).iter_batches(batch_size=2))
    # 3 seeded rows, batch_size=2 -> [2, 1]
    assert [len(b) for b in batches] == [2, 1]


def test_query_handle_repr_shows_resolved_id_after_use(cf) -> None:
    client, mock = cf
    _seed_orders(mock)
    mock.seed_query(QID, collection=CID, id=QID)
    q = client.data.query(QID)
    assert "->" not in repr(q)  # unresolved before use
    q.read()
    assert f"-> {QID}" in repr(q)  # resolved id shown after use
