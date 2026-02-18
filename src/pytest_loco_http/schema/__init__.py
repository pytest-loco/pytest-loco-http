"""HTTP-related plugin models.

This module defines immutable Pydantic models used to represent HTTP
entities such as cookies, URLs, requests, and responses. These models
serve as normalized and structured representations of objects coming
from external libraries like `requests` or `http.cookiejar`.
"""

from .cookies import CookieModel
from .files import FileModel, FilesModel
from .requests import RequestModel, ResponseModel
from .urls import UrlModel

__all__ = (
    'CookieModel',
    'FileModel',
    'FilesModel',
    'RequestModel',
    'ResponseModel',
    'UrlModel',
)
