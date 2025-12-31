import os
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from app.domain.models import Application
from app.application.interfaces.repository import IApplicationRepository


class MongoApplicationRepository(IApplicationRepository):

    def __init__(self, client: AsyncIOMotorClient, db_name: str):
        # Use the passed db_name to select the database
        self.db = client[db_name]
        self.collection = self.db["applications"]

    def _map_to_domain(self, doc: dict) -> Application:
        if not doc:
            return None
        doc["id"] = str(doc["_id"])
        return Application(**doc)

    async def save(self, app: Application) -> Application:
        app_dict = app.dict(exclude={"id"})
        if app.id:
            await self.collection.update_one(
                {"_id": ObjectId(app.id)}, {"$set": app_dict}
            )
            return app
        else:
            result = await self.collection.insert_one(app_dict)
            app.id = str(result.inserted_id)
            return app

    async def get_by_id(self, app_id: str) -> Optional[Application]:
        try:
            oid = ObjectId(app_id)
        except Exception:
            return None
        doc = await self.collection.find_one({"_id": oid})
        return self._map_to_domain(doc)

    async def get_by_job(self, job_id: str) -> List[Application]:
        cursor = self.collection.find({"job_id": job_id})
        apps = []
        async for doc in cursor:
            apps.append(self._map_to_domain(doc))
        return apps

    async def get_by_candidate(self, candidate_id: str) -> List[Application]:
        cursor = self.collection.find({"candidate_id": candidate_id})
        apps = []
        async for doc in cursor:
            apps.append(self._map_to_domain(doc))
        return apps

    async def delete(self, app_id: str) -> bool:
        try:
            oid = ObjectId(app_id)
        except Exception:
            return False
        result = await self.collection.delete_one({"_id": oid})
        return result.deleted_count > 0

    async def delete_by_job(self, job_id: str) -> int:
        result = await self.collection.delete_many({"job_id": job_id})
        return result.deleted_count

    async def delete_by_candidate(self, candidate_id: str) -> int:
        result = await self.collection.delete_many({"candidate_id": candidate_id})
        return result.deleted_count
