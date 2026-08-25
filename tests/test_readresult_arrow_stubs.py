"""Reserved Arrow output surfaces on ``ReadResult``.

The Arrow read path is server-gated: this client version always reads JSON, so
``to_arrow`` / ``to_polars`` / ``__arrow_c_stream__`` exist but do not yet
produce a result. They must fail *loudly and helpfully* rather than as a bare
``AttributeError``:

* dependency missing  -> ``ClappformError`` telling you to ``pip install`` the
  right extra (lazy import, same pattern as ``to_pandas``);
* dependency present  -> ``NotImplementedError`` saying server Arrow support
  has not shipped.

These tests pin both branches deterministically regardless of whether pyarrow /
polars happen to be installed in the test environment.
"""

from __future__ import annotations

import builtins

import pytest

from clappform._codec import ChunkFormat
from clappform._errors import ClappformError
from clappform.dataframes import ReadResult


def _empty_result() -> ReadResult:
    return ReadResult(iter([(ChunkFormat.JSON, b"[]")]))


def _hide_module(monkeypatch: pytest.MonkeyPatch, name: str) -> None:
    """Make ``import <name>`` raise ImportError, even if it is installed."""
    real_import = builtins.__import__

    def fake_import(mod, *args, **kwargs):
        if mod == name or mod.startswith(name + "."):
            raise ImportError(f"{name} hidden for test")
        return real_import(mod, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)


def _provide_module(monkeypatch: pytest.MonkeyPatch, name: str) -> None:
    """Ensure ``import <name>`` succeeds, injecting a stub if not installed."""
    import sys
    import types

    if name not in sys.modules:
        monkeypatch.setitem(sys.modules, name, types.ModuleType(name))


# --- missing-dependency branch: friendly install hint -----------------------

def test_to_arrow_without_pyarrow_points_at_the_extra(monkeypatch: pytest.MonkeyPatch) -> None:
    _hide_module(monkeypatch, "pyarrow")
    with pytest.raises(ClappformError, match=r"clappform\[arrow\]"):
        _empty_result().to_arrow()


def test_to_polars_without_polars_points_at_the_extra(monkeypatch: pytest.MonkeyPatch) -> None:
    _hide_module(monkeypatch, "polars")
    with pytest.raises(ClappformError, match=r"clappform\[polars\]"):
        _empty_result().to_polars()


def test_arrow_stream_without_pyarrow_points_at_the_extra(monkeypatch: pytest.MonkeyPatch) -> None:
    _hide_module(monkeypatch, "pyarrow")
    with pytest.raises(ClappformError, match=r"clappform\[arrow\]"):
        _empty_result().__arrow_c_stream__()


# --- dependency-present branch: server not ready yet ------------------------

def test_to_arrow_with_pyarrow_reports_server_not_ready(monkeypatch: pytest.MonkeyPatch) -> None:
    _provide_module(monkeypatch, "pyarrow")
    with pytest.raises(NotImplementedError, match="not available yet"):
        _empty_result().to_arrow()


def test_to_polars_with_polars_reports_server_not_ready(monkeypatch: pytest.MonkeyPatch) -> None:
    _provide_module(monkeypatch, "polars")
    with pytest.raises(NotImplementedError, match="not available yet"):
        _empty_result().to_polars()


def test_arrow_stream_with_pyarrow_reports_not_ready(monkeypatch: pytest.MonkeyPatch) -> None:
    _provide_module(monkeypatch, "pyarrow")
    with pytest.raises(NotImplementedError, match="not available yet"):
        _empty_result().__arrow_c_stream__()


# --- reserved, not AttributeError -------------------------------------------

def test_reserved_methods_exist_rather_than_attributeerror() -> None:
    # The whole point of Phase 0: the names are present so callers discover the
    # capability and get a clear message, never a bare AttributeError.
    result = _empty_result()
    for name in ("to_arrow", "to_polars", "__arrow_c_stream__"):
        assert callable(getattr(result, name))
