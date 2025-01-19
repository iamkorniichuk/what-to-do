from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

import magic


@deconstructible
class ContentTypeValidator:
    def __init__(self, *content_types):
        self.content_types = content_types

    def __call__(self, file):
        mime_type = magic.from_buffer(file.read(2048), mime=True)

        if mime_type not in self.content_types:
            allowed_content_types = ", ".join(self.content_types)
            raise ValidationError(
                f"Allowed content types: {allowed_content_types}. Current content type: {mime_type}"
            )

    def __eq__(self, other):
        return self.content_types == other.content_types


@deconstructible
class FileSizeValidator:
    def __init__(self, max_file_size):
        self.max_file_size = max_file_size

    def __call__(self, file):
        file_size = file.size or file._size

        if file_size > self.max_file_size:
            raise ValidationError(
                f"Max file size: {self.max_file_size}B. Current file size: {file_size}B"
            )

    def __eq__(self, other):
        return self.max_file_size == other.max_file_size
