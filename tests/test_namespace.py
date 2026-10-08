"""Namespace discoverability: wrong-family hints, dir(), help(), shortcuts.

The public surface stays two levels deep (``cf.data.insert``) because names are
only unique at the gRPC-path level. These tests pin the ergonomics that make
the split friendly: reach for a name on the wrong object and you are told its
real home; colliding names name *every* owning family; the curated shortcut
allowlist never hoists an ambiguous name.
"""

from __future__ import annotations

import pytest

from clappform import Clappform, ConfigurationError, _namespace


class _NullTransport:
    def invoke(self, *args, **kwargs):
        raise RuntimeError("no RPC should be attempted in these tests")


def make_client() -> Clappform:
    return Clappform("acme", "qa", api_key="k", transport=_NullTransport())


# --- the derived index -------------------------------------------------------

def test_index_is_derived_from_api_families_not_hand_maintained() -> None:
    # A representative service/method from each family must appear, proving the
    # index is built by introspecting API_FAMILIES rather than a static list.
    index = _namespace.name_index()
    assert "insert" in index          # data method
    assert "aggregate" in index       # data service
    assert index["insert"] == ["data"]


def test_colliding_names_list_all_owning_families() -> None:
    index = _namespace.name_index()
    # These service names exist on more than one family (different hosts).
    assert index["general"] == ["auth", "client", "data", "notifier"]
    assert index["process"] == ["client", "data"]
    assert index["version"] == ["auth", "client"]


def test_index_is_cached() -> None:
    assert _namespace.name_index() is _namespace.name_index()


# --- hints -------------------------------------------------------------------

def test_hint_for_unique_name_names_the_one_family() -> None:
    hint = _namespace.wrong_family_hint("insert")
    assert "cf.data" in hint
    assert "not on the client directly" in hint


def test_hint_for_colliding_name_names_every_family() -> None:
    hint = _namespace.wrong_family_hint("process")
    assert "cf.client" in hint and "cf.data" in hint


def test_hint_for_unknown_name_is_none() -> None:
    assert _namespace.wrong_family_hint("definitely_not_a_service") is None


# --- client integration ------------------------------------------------------

def test_wrong_family_access_raises_with_hint() -> None:
    cf = make_client()
    with pytest.raises(AttributeError, match=r"insert.*lives on cf\.data"):
        cf.insert  # noqa: B018 - the access itself is what triggers __getattr__


def test_colliding_access_lists_families() -> None:
    cf = make_client()
    with pytest.raises(AttributeError, match=r"cf\.client.*cf\.data|cf\.data.*cf\.client"):
        cf.process  # noqa: B018 - the access itself is what triggers __getattr__


def test_genuine_typo_gets_plain_attribute_error() -> None:
    cf = make_client()
    with pytest.raises(AttributeError, match="has no attribute 'totally_made_up'"):
        cf.totally_made_up  # noqa: B018 - the access itself is what triggers __getattr__


def test_private_attribute_miss_stays_a_plain_attributeerror() -> None:
    # Dunder / private probes (copy, pickle, hasattr on internals) must miss
    # cleanly without going through the hint machinery.
    cf = make_client()
    with pytest.raises(AttributeError):
        cf.__wrapped__  # noqa: B018
    assert not hasattr(cf, "_not_a_real_private_attr")


def test_dir_lists_the_four_families() -> None:
    cf = make_client()
    listing = set(dir(cf))
    assert {"data", "client", "auth", "notifier"} <= listing


def test_help_without_argument_lists_families() -> None:
    cf = make_client()
    summary = cf.help()
    for family in ("cf.data", "cf.client", "cf.auth", "cf.notifier"):
        assert family in summary


def test_help_with_name_returns_the_hint() -> None:
    cf = make_client()
    assert "cf.data" in cf.help("insert")
    assert "not a known" in cf.help("definitely_not_a_service")


# --- canonical path stays intact --------------------------------------------

def test_dataframe_entry_points_stay_on_cf_data() -> None:
    cf = make_client()
    assert callable(cf.data.collection)
    assert callable(cf.data.query)


def test_shortcut_allowlist_is_empty_by_default() -> None:
    # Nothing is hoisted yet: collection/query are ambiguous (also on cf.client),
    # so they stay at cf.data.* until a reviewed, unambiguous name is added.
    assert Clappform._SHORTCUTS == {}


# --- shortcut guard ----------------------------------------------------------

def test_guard_refuses_to_hoist_an_ambiguous_shortcut(monkeypatch: pytest.MonkeyPatch) -> None:
    # 'process' lives on both cf.client and cf.data; trying to hoist it must
    # fail loudly rather than silently shadow one family.
    monkeypatch.setattr(Clappform, "_SHORTCUTS", {"process": "data"})
    with pytest.raises(ConfigurationError, match="ambiguous shortcut 'process'"):
        make_client()


def test_guard_rejects_a_shortcut_absent_from_its_family(monkeypatch: pytest.MonkeyPatch) -> None:
    # A shortcut naming nothing on its declared family (a typo'd allowlist
    # entry) must fail with a clear config error, not a raw AttributeError
    # from deep in service binding.
    monkeypatch.setattr(Clappform, "_SHORTCUTS", {"no_such_entry_point": "data"})
    with pytest.raises(ConfigurationError, match="cannot hoist shortcut 'no_such_entry_point'"):
        make_client()
