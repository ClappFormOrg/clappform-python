"""Test doubles for the Clappform client.

:class:`LocalMock` is a transport double that plugs into
``Clappform(transport=LocalMock())``. It serves canned responses, records
calls for assertions, and can seed collections so DataFrame round-trips run
without infrastructure — used by our tests, by customers testing pipelines,
and by ``examples/`` so the documented examples actually execute. The
transport seam it implements lives in :mod:`clappform._runtime`.
"""

from clappform.testing._local_mock import LocalMock, RecordedCall

__all__ = ["LocalMock", "RecordedCall"]
