"""HTTP plugin for pytest-loco DSL.

This plugin provides first-class HTTP support for the pytest-loco domain-
specific language. It exposes a set of HTTP method actors (GET, POST, PUT,
PATCH, DELETE, etc.) that allow test scenarios to perform real HTTP requests
through managed sessions.

The plugin registers HTTP method actors under the "http" namespace and
integrates seamlessly with the pytest-loco extension system.
"""

from pytest_loco.extensions import Plugin

from .actions import actors
from .instructions import urljoin_

http = Plugin(
    name='http',
    actors=actors,
    instructions=[urljoin_],
)
