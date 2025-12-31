from typing import Any
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from bson import ObjectId
from app.application.interfaces.file_store import IFileStore


class GridFSFileStore(IFileStore):
    def __init__(self, bucket: AsyncIOMotorGridFSBucket):
        self.bucket = bucket

    async def upload_file(
        self, filename: str, content: bytes, content_type: str
    ) -> str:
        # Upload from bytes
        grid_in = self.bucket.open_upload_stream(
            filename, metadata={"contentType": content_type}
        )
        await grid_in.write(content)
        await grid_in.close()
        return str(grid_in._id)

    async def download_file(self, file_id: str) -> Any:
        try:
            oid = ObjectId(file_id)
        except Exception:
            return None

        # Open download stream
        try:
            grid_out = await self.bucket.open_download_stream(oid)
            return grid_out
        except Exception:
            return None

    async def delete_file(self, file_id: str) -> bool:
        try:
            oid = ObjectId(file_id)
            await self.bucket.delete(oid)
            return True
        except Exception:
            return False
