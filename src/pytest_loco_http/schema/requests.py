"""HTTP request and response models."""

from http import HTTPMethod, HTTPStatus
from typing import TYPE_CHECKING, Any

from pydantic import Field
from requests import Request

from pytest_loco_http.models import PluginModel, Url

from .cookies import CookieModel
from .urls import UrlModel

if TYPE_CHECKING:
    from typing import Self

if TYPE_CHECKING:
    from requests import PreparedRequest, Response


class RequestModel(PluginModel):
    """Structured representation of an HTTP request.

    The model normalizes request method, headers, cookies, body,
    and URL components into immutable form.
    """

    method: HTTPMethod = Field(
        title='HTTP method',
        description='The HTTP method of the request.',
    )

    url_string: Url = Field(
        serialization_alias='urlString',
        title='Request URL',
        description='The full request URL as a validated HttpUrl.',
    )
    url: UrlModel = Field(
        title='Parsed URL',
        description='Structured representation of the request URL.',
    )

    headers: dict[str, str] = Field(
        default_factory=dict,
        title='Headers',
        description='Request headers normalized to lowercase keys.',
    )

    cookies: list[CookieModel] = Field(
        default_factory=list,
        title='Cookies',
        description='List of cookies attached to the request.',
    )

    body: bytes | None = Field(
        default=None,
        title='Request body',
        description='The raw request body as bytes.',
    )

    text: str | None = Field(
        default=None,
        title='Request body text',
        description='The raw request body as text.',
    )

    @classmethod
    def from_request(cls, request: 'PreparedRequest | Request') -> 'Self':
        """Create a RequestModel from a requests request object.

        Args:
            request: A Request or PreparedRequest instance.

        Returns:
            A normalized RequestModel instance.
        """
        if isinstance(request, Request):
            request = request.prepare()

        data: dict[str, Any] = {
            'method': HTTPMethod(request.method or 'GET'),
            'headers': {
                key.lower(): value
                for key, value in request.headers.items()
            },
        }

        if request.url:
            data.setdefault('url_string', request.url)
            data.setdefault('url', UrlModel.from_value(request.url))

        if request.body is not None:
            content = request.body
            if isinstance(content, str):
                data.setdefault('text', content)
                content = content.encode()

            data.setdefault('body', content)

        if cookiejar := getattr(request, '_cookies', None):
            data.setdefault('cookies', [
                CookieModel.from_cookiejar_cookie(cookie)
                for cookie in cookiejar
            ])

        return cls.model_validate(data)


class ResponseModel(PluginModel):
    """Structured representation of an HTTP response.

    The model normalizes status code, headers, cookies, response body,
    and redirect history into immutable form.
    """

    status: HTTPStatus = Field(
        title='HTTP status',
        description='The HTTP status code of the response.',
    )

    headers: dict[str, str] = Field(
        default_factory=dict,
        title='Headers',
        description='Response headers normalized to lowercase keys.',
    )

    cookies: list[CookieModel] = Field(
        default_factory=list,
        title='Cookies',
        description='List of cookies set by the response.',
    )

    body: bytes | None = Field(
        default=None,
        title='Response body',
        description='The raw response body as bytes.',
    )

    text: str | None = Field(
        default=None,
        title='Response body text',
        description='The raw response body as text.',
    )

    request: RequestModel = Field(
        title='Original request.',
        description='The HTTP request that resulted in this response.',
    )

    history: list['ResponseModel'] = Field(
        default_factory=list,
        title='Redirect history',
        description='List of previous responses in redirect chain.',
    )

    @classmethod
    def from_response(cls, response: 'Response') -> 'Self':
        """Create a ResponseModel from a requests Response object.

        Args:
            response: A Response instance.

        Returns:
            A normalized ResponseModel instance.
        """
        data: dict[str, Any] = {
            'status': HTTPStatus(response.status_code),
            'request': RequestModel.from_request(response.request),
            'headers': {
                key.lower(): value
                for key, value in response.headers.items()
            },
        }

        if response.content:
            data.setdefault('body', response.content)
            data.setdefault('text', response.text)

        if response.cookies:
            data.setdefault('cookies', [
                CookieModel.from_cookiejar_cookie(cookie)
                for cookie in response.cookies
            ])

        if response.history:
            data.setdefault('history', [
                cls.from_response(subresponse)
                for subresponse in response.history
            ])

        return cls.model_validate(data)
