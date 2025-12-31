from abc import ABC, abstractmethod
from typing import Any


class IFileStore(ABC):
    """
    Interface for File Storage (Resume PDFs).
    """

    @abstractmethod
    async def upload_file(
        self, filename: str, content: bytes, content_type: str
    ) -> str:
        """
        Uploads a file and returns the unique File ID (e.g., GridFS ID).
        """
        pass

    @abstractmethod
    async def download_file(self, file_id: str) -> Any:
        """
        Retrieves the file stream or bytes.
        """
        pass

    @abstractmethod
    async def delete_file(self, file_id: str) -> bool:
        """
        Permanently removes a file from storage.
        """
        pass
