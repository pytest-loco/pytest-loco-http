"""Base Pydantic model and fields for HTTP plugin entities."""

from pathlib import Path
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, FilePath, HttpUrl, PlainSerializer


def stringify(value: Any) -> str | Any:  # noqa: ANN401
    """Stringify value."""
    if isinstance(value, (Path, HttpUrl)):
        return str(value)

    return value


Stringify = PlainSerializer(stringify, return_type=str)

File = Annotated[FilePath, Stringify]
Url = Annotated[HttpUrl, Stringify]


class PluginModel(BaseModel):
    """Base model for HTTP plugin entities.

    The model is immutable and ignores unknown fields. It is intended
    to provide a stable and normalized representation of external HTTP
    objects.
    """

    model_config = ConfigDict(
        extra='ignore',
        frozen=True,
        validate_default=False,
    )
