"""Cluster discovery from the location's CNAME target.

All tests inject a stub resolver — no live DNS is ever performed in CI.
"""

import socket

import pytest

from clappform._discovery import discover_cluster
from clappform._errors import ClappformError, ConfigurationError


def test_main_cluster_resolves_to_empty_extension() -> None:
    resolver = lambda host: "bigip.clappform.com"  # noqa: E731
    assert discover_cluster("gelderland", resolver=resolver) == ""


def test_suffixed_cluster_extension_extracted() -> None:
    resolver = lambda host: "bigip-prod-lts.clappform.com"  # noqa: E731
    assert discover_cluster("noord-brabant", resolver=resolver) == "prod-lts"


def test_queried_host_is_location_under_base_domain() -> None:
    seen: list[str] = []

    def resolver(host: str) -> str:
        seen.append(host)
        return "bigip-qa.clappform.com"

    assert discover_cluster("acme", resolver=resolver) == "qa"
    assert seen == ["acme.clappform.com"]


def test_fqdn_trailing_dot_and_case_are_tolerated() -> None:
    resolver = lambda host: "BigIP-QA-LTS.Clappform.com."  # noqa: E731
    assert discover_cluster("acme", resolver=resolver) == "qa-lts"


def test_nxdomain_raises_configuration_error_with_hint() -> None:
    def resolver(host: str) -> str:
        raise socket.gaierror(8, "nodename nor servname provided")

    with pytest.raises(ConfigurationError, match="pass cluster= explicitly") as excinfo:
        discover_cluster("does-not-exist", resolver=resolver)
    assert "does-not-exist.clappform.com" in str(excinfo.value)


def test_non_bigip_canonical_name_is_rejected() -> None:
    resolver = lambda host: "some-other-lb.example.net"  # noqa: E731
    with pytest.raises(ConfigurationError, match="does not match"):
        discover_cluster("acme", resolver=resolver)


def test_musl_style_echo_of_query_is_rejected_not_misread() -> None:
    # musl resolvers report no canonical name and echo the queried host back;
    # that must land in the fail-loud path, never be parsed as a cluster.
    resolver = lambda host: host  # noqa: E731
    with pytest.raises(ConfigurationError, match="pass cluster= explicitly"):
        discover_cluster("acme", resolver=resolver)


@pytest.mark.parametrize("location", ["", "acme.clappform.com", "bad_label", "a b"])
def test_invalid_location_labels_fail_before_any_lookup(location: str) -> None:
    def resolver(host: str) -> str:
        raise AssertionError("resolver must not be called for invalid labels")

    with pytest.raises(ConfigurationError, match="not a valid"):
        discover_cluster(location, resolver=resolver)


def test_errors_are_catchable_as_clappform_error() -> None:
    resolver = lambda host: "wrong.example.com"  # noqa: E731
    with pytest.raises(ClappformError):
        discover_cluster("acme", resolver=resolver)
