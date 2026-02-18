"""HTTP session management utilities.

This module provides a centralized session manager responsible for
creating and caching configured `requests.Session` instances.
Sessions are identified by name and reused across the application.
"""

from typing import ClassVar

from requests import Session

from .user_agent import LOCO_USER_AGENT


class SessionManager:
    """Factory and registry for configured HTTP sessions.

    This class maintains a cache of named `requests.Session` instances.
    If a session with a given name does not exist, it is created and stored.
    Subsequent calls with the same name return the cached instance.

    Sessions are initialized with a predefined User-Agent header.
    """

    _sessions: ClassVar[dict[str, Session]] = {}

    @staticmethod
    def initialize() -> Session:
        """Create and configure a new HTTP session.

        The session is initialized with the default User-Agent header.

        Returns:
            A configured `requests.Session` instance.
        """
        session = Session()
        session.headers = {'user-agent': LOCO_USER_AGENT}

        return session

    @classmethod
    def get_session(cls, name: str = 'default') -> Session:
        """Retrieve a named HTTP session.

        If a session with the specified name does not exist,
        a new one is created and cached.

        Args:
            name: The logical name of the session.

        Returns:
            A cached or newly created `requests.Session` instance.
        """
        if name not in cls._sessions:
            cls._sessions[name] = cls.initialize()

        return cls._sessions[name]
