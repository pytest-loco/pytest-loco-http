"""HTTP request actors for pytest-loco integration.

This module defines generic HTTP actions for all HTTP methods.
Each action delegates execution to a shared request function and
returns a normalized ResponseModel dump.
"""

from functools import partial
from http import HTTPMethod
from typing import TYPE_CHECKING

from pytest_loco.extensions import Actor, Attribute, Schema
from pytest_loco.values import Deferred, Value

from .models import File, Url
from .schema import FilesModel, ResponseModel
from .sessions import SessionManager

if TYPE_CHECKING:
    from collections.abc import Mapping

if TYPE_CHECKING:
    from pytest_loco.values import RuntimeValue

def request(method: str, params: 'Mapping[str, RuntimeValue]') -> 'RuntimeValue':
    """Execute an HTTP request using a managed session.

    The function extracts supported request parameters, performs
    an HTTP call via `requests.Session`, and returns a serialized
    normalized response.

    Args:
        method: HTTP method to execute.
        params: Runtime-evaluated parameters for the request.

    Returns:
        A serialized response.
    """
    payload = {
        key: value
        for key, value in params.items()
        if key in {
            'url',
            'params',
            'data',
            'headers',
            'timeout',
            'verify',
        }
    }

    if files := params.get('files'):
        attachments = FilesModel.model_validate(files).to_requests()
        payload['files'] = attachments

    response = (
        SessionManager.get_session(params.get('session', 'default'))
        .request(method, **payload)
    )

    return (
        ResponseModel
        .from_response(response)
        .model_dump()
    )


request_parameters = Schema({
    'session': Attribute(
        base=str,
        default='default',
        title='Session name',
        description='Logical name of the HTTP session to use.',
    ),
    'url': Attribute(
        base=Url,
        required=True,
        title='Request URL',
        description='Target URL for the HTTP request.',
    ),
    'headers': Attribute(
        base=dict[str, Deferred[Value]],
        deferred=False,
        title='Headers',
        description='Optional HTTP headers to include in the request.',
    ),
    'params': Attribute(
        base=dict[str, Deferred[Value]],
        aliases=['query', 'queryParams'],
        deferred=False,
        title='Query parameters',
        description='URL query parameters appended to the request.',
    ),
    'data': Attribute(
        base=bytes | str,
        title='Request body',
        description='Optional request payload as raw bytes or string.',
    ),
    'timeout': Attribute(
        base=int | float,
        title='Timeout',
        description='Response timeout.',
    ),
    'files': Attribute(
        base=FilesModel,
        default=None,
        deferred=False,
        title='Multipart files',
        description='Optional multipart file attachments.',
    ),
    'verify': Attribute(
        base=bool | File,
        aliases=['sslVerify', 'caBundle'],
        default=True,
        title='SSL verification',
        description=(
            'SSL verification setting.\n'
            'Can be a boolean or a path to a CA bundle file.'
        ),
    ),
})


actors = [
    Actor(
        actor=partial(request, method.name),
        name=method.name.lower(),
        parameters=request_parameters,
    )
    for method in HTTPMethod
]
