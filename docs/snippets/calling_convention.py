"""Runnable source for the calling-convention section of the API families page."""

from __future__ import annotations

from clappform.testing import LocalMock


def build_mock() -> LocalMock:
    from clappform.gen.clappform.client.v1.actionflow import actionflow_pb2
    from clappform.gen.clappform.client.v1.actionflow_task import actionflow_task_pb2
    from clappform.gen.clappform.data.v1.usage import usage_pb2

    mock = LocalMock()
    mock.on(
        "/clappform.client.v1.actionflow.ActionflowManagement/Start",
        actionflow_pb2.StartActionflowResponse(message="started", uuid="run-1"),
    )
    mock.on(
        "/clappform.client.v1.actionflow_task.ActionflowTaskManagement/Create",
        lambda request: actionflow_task_pb2.ActionflowTask(name=request.name),
    )
    mock.on(
        "/clappform.data.v1.usage.UsageManagement/GetQueryUsage",
        usage_pb2.QueryUsageResponse(),
    )
    return mock


def run(transport: LocalMock) -> None:
    from clappform import Clappform

    with Clappform(location="acme", api_key="cf_live_...", transport=transport) as cf:
        # --8<-- [start:message-or-kwargs]
        from clappform.gen.clappform.client.v1.actionflow import actionflow_pb2

        cf.client.actionflow.start(id="recalculate-dashboards")
        cf.client.actionflow.start(actionflow_pb2.StartActionflow(id="recalculate-dashboards"))
        # --8<-- [end:message-or-kwargs]
        assert transport.calls[-1].request == transport.calls[-2].request

        query_id = "4a4f9a52-0000-4000-8000-000000000002"
        # --8<-- [start:underscore]
        from datetime import datetime, timezone

        cf.client.actionflow_task.create(name="export", timeout_=300)  # the task's timeout field
        since = datetime(2026, 1, 1, tzinfo=timezone.utc)
        cf.data.usage.get_query_usage(query_id=query_id, from_={"seconds": int(since.timestamp())})
        # --8<-- [end:underscore]
        create = next(c for c in transport.calls if c.method.endswith("/Create"))
        assert create.request.timeout == 300 and create.timeout is None
        assert getattr(transport.calls[-1].request, "from").seconds == int(since.timestamp())

        calls_before = len(transport.calls)
        # --8<-- [start:oneof]
        try:
            cf.data.export.create_export(inline={}, saved_query={})
        except TypeError as exc:
            print(exc)  # ...belong to the oneof 'pipeline_source'; pass only one of them
        # --8<-- [end:oneof]
        assert len(transport.calls) == calls_before  # refused before any call


if __name__ == "__main__":
    run(build_mock())
