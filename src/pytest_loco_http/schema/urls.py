"""URL model for normalized HTTP URL representation."""

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field, SecretStr
from yarl import URL

from pytest_loco_http.models import PluginModel

if TYPE_CHECKING:
    from typing import Self


class UrlModel(PluginModel):
    """Structured representation of an HTTP URL.

    The model extracts normalized URL components from a string and
    represents them in structured form.
    """

    scheme: Literal['http', 'https'] = Field(
        title='URL scheme',
        description='The URL scheme (http or https).',
    )

    user: str | None = Field(
        default=None,
        title='Username',
        description='The username component of the URL, if present.',
    )
    password: SecretStr | None = Field(
        default=None,
        title='Password',
        description='The password component of the URL, stored as secret.',
    )

    host: str | None = Field(
        default=None,
        title='Host',
        description='The host component of the URL.',
    )

    port: int | None = Field(
        default=None,
        ge=0,
        le=65535,
        title='Port',
        description='The network port of the URL.',
    )

    path: str = Field(
        title='Path',
        description='The path component of the URL.',
    )

    query_string: str | None = Field(
        default=None,
        title='Query string',
        description='The raw query string portion of the URL.',
    )
    query: dict[str, Any] = Field(
        default_factory=dict,
        title='Query parameters',
        description='Parsed query parameters as a dictionary.',
    )

    fragment: str | None = Field(
        default=None,
        title='Fragment',
        description='The fragment identifier of the URL.',
    )

    @classmethod
    def from_value(cls, value: str) -> 'Self':
        """Create a UrlModel from a URL string.

        Args:
            value: A URL string.

        Returns:
            A normalized UrlModel instance.
        """
        url = URL(value)

        data: dict[str, Any] = {
            key: getattr(url, key)
            for key in (
                'scheme',
                'user',
                'host',
                'port',
                'path',
                'query_string',
                'fragment',
            )
        }

        if url.password:
            data.setdefault('password', SecretStr(url.password))
        if url.query_string:
            data.setdefault('query', dict(url.query))

        return cls.model_validate(data)
