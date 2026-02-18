"""HTTP cookie model."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from pydantic import Field, SecretStr

from pytest_loco_http.models import PluginModel

if TYPE_CHECKING:
    from http.cookiejar import Cookie
    from typing import Self


class CookieModel(PluginModel):
    """Structured representation of an HTTP cookie.

    This model mirrors relevant attributes from `http.cookiejar.Cookie`
    and converts them into an immutable Pydantic-compatible form.
    """

    version: int | None = Field(
        default=None,
        title='Cookie version',
        description='The cookie specification version.',
    )

    name: str = Field(
        title='Cookie name',
        description='The name of the cookie.',
    )

    value: SecretStr | None = Field(
        default=None,
        title='Cookie value',
        description='The value of the cookie. Stored as a secret string.',
    )

    domain: str | None = Field(
        default=None,
        title='Cookie domain',
        description='The domain for which the cookie is valid.',
    )

    port: int | None = Field(
        default=None,
        ge=0,
        le=65535,
        title='Cookie port',
        description='The port for which the cookie is valid.',
    )

    path: str | None = Field(
        default=None,
        title='Cookie path',
        description='The URL path for which the cookie is valid.',
    )

    secure: bool = Field(
        default=False,
        title='Secure flag',
        description='Indicates whether the cookie is restricted to HTTPS.',
    )

    discard: bool = Field(
        default=False,
        title='Discard flag',
        description='Indicates whether the cookie should be discarded at session end.',
    )

    expires: datetime | None = Field(
        default=None,
        title='Expiration time',
        description='The expiration time of the cookie as a datetime object.',
    )

    comment: str | None = Field(
        default=None,
        title='Cookie comment',
        description='Optional comment associated with the cookie.',
    )

    comment_url: str | None = Field(
        default=None,
        title='Comment URL',
        description='URL providing additional information about the cookie.',
    )

    rest: dict[str, Any] = Field(
        default_factory=dict,
        validation_alias='_rest',
        title='Additional attributes',
        description='Additional non-standard cookie attributes.',
    )

    @classmethod
    def from_cookiejar_cookie(cls, cookie: 'Cookie') -> 'Self':
        """Create a CookieModel from a Cookie instance.

        Args:
            cookie: A cookie instance from http.cookiejar.

        Returns:
            An immutable CookieModel instance.
        """
        data: dict[str, Any] = {
            key: getattr(cookie, key)
            for key in (
                'version',
                'name',
                'secure',
                'discard',
                'comment',
                'comment_url',
                '_rest',
            )
        }

        if cookie.value is not None:
            data.setdefault('value', SecretStr(cookie.value))

        if cookie.domain_specified:
            data.setdefault('domain', cookie.domain)
        if cookie.port_specified:
            data.setdefault('port', cookie.port)
        if cookie.path_specified:
            data.setdefault('path', cookie.path)

        if cookie.expires is not None:
            data.setdefault('expires', datetime.fromtimestamp(cookie.expires, tz=UTC))

        return cls.model_validate(data)
