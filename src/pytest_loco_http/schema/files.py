"""File attachment models for HTTP requests."""

from pydantic import ConfigDict, Field, RootModel

from pytest_loco_http.models import PluginModel

type Attachment = tuple[str | None, str | bytes, str | None]
type Attachments = dict[str, Attachment]


SIMPLE_CHARS = r'[a-zA-Z0-9_\-\.]+'


class FileModel(PluginModel):
    """Structured representation of a multipart file field.

    This model represents a single file entry suitable for inclusion
    in a multipart/form-data request.
    """

    name: str = Field(
        pattern=rf'^{SIMPLE_CHARS}$',
        title='Form field name',
        description='The multipart form field name for the file.',
    )

    content: str | bytes = Field(
        title='File content',
        description='The file content as text or raw bytes.',
    )

    filename: str | None = Field(
        default=None,
        pattern=rf'^{SIMPLE_CHARS}$',
        title='Filename',
        description='Optional filename reported in the multipart payload.',
    )

    mimetype: str | None = Field(
        default=None,
        pattern=rf'^{SIMPLE_CHARS}/{SIMPLE_CHARS}$',
        title='MIME type',
        description='Optional MIME type of the file (e.g., text/plain).',
    )

    @property
    def content_type(self) -> str | None:
        """Infer the content type for the file.

        Resolution order:
            1. Explicit `mimetype` if provided.
            2. `application/octet-stream` for byte content.
            3. `text/plain` for string content.

        Returns:
            The resolved content type string, or None if it cannot be determined.
        """
        if self.mimetype:
            return self.mimetype

        if isinstance(self.content, bytes):
            return 'application/octet-stream'

        if isinstance(self.content, str):
            return 'text/plain'



class FilesModel(RootModel[list[FileModel]]):
    """Collection of multipart file models."""

    model_config = ConfigDict(title='Files')

    def to_requests(self) -> Attachments | None:
        """Convert files into requests-compatible attachment mapping.

        Returns:
            A dictionary suitable for the `files` parameter of
            `requests.request`. Returns None if no files are present.
        """
        if not self.root:
            return None

        return {
            file.name: (
                file.filename or file.name,
                file.content,
                file.content_type,
            )
            for file in self.root
        }
