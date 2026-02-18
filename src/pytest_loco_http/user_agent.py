"""User-Agent construction utilities.

This module builds a standardized User-Agent string used by the
HTTP integration layer. The value includes version information for
the main package, its HTTP plugin, and the underlying requests library.
"""

from importlib.metadata import version

from requests_toolbelt.utils.user_agent import user_agent

LOCO_PACKAGE = 'pytest-loco'
LOCO_PLUGIN = 'pytest-loco-http'
REQUESTS_PACKAGE = 'requests'

LOCO_USER_AGENT = user_agent(
    LOCO_PACKAGE, version(LOCO_PACKAGE),
    extras=(
        (LOCO_PLUGIN, version(LOCO_PLUGIN)),
        (REQUESTS_PACKAGE, version(REQUESTS_PACKAGE)),
    ),
)
