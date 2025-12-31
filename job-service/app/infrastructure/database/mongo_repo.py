import os
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId, Regex

from app.domain.models import Job
from app.application.interfaces.repository import IJobRepository


class MongoJobRepository(IJobRepository):

    def __init__(self, client: AsyncIOMotorClient, db_name: str):
        # Use the passed db_name to select the database
        self.db = client[db_name]
        self.collection = self.db["jobs"]

    def _map_to_domain(self, doc: dict) -> Job:
        if not doc:
            return None
        doc["id"] = str(doc["_id"])
        return Job(**doc)

    async def save(self, job: Job) -> Job:
        job_dict = job.dict(exclude={"id"})
        if job.id:
            await self.collection.update_one(
                {"_id": ObjectId(job.id)}, {"$set": job_dict}
            )
            return job
        else:
            result = await self.collection.insert_one(job_dict)
            job.id = str(result.inserted_id)
            return job

    async def get_by_id(self, job_id: str) -> Optional[Job]:
        try:
            oid = ObjectId(job_id)
        except Exception:
            return None
        doc = await self.collection.find_one({"_id": oid})
        return self._map_to_domain(doc)

    async def get_all(self, limit: int = 10, offset: int = 0) -> List[Job]:
        cursor = self.collection.find().skip(offset).limit(limit)
        jobs = []
        async for doc in cursor:
            jobs.append(self._map_to_domain(doc))
        return jobs

    async def search(self, query: str) -> List[Job]:
        # Simple regex search on title or description
        regex = Regex(query, "i")
        cursor = self.collection.find(
            {"$or": [{"title": regex}, {"description": regex}]}
        )
        jobs = []
        async for doc in cursor:
            jobs.append(self._map_to_domain(doc))
        return jobs

    async def delete(self, job_id: str) -> bool:
        try:
            oid = ObjectId(job_id)
        except Exception:
            return False
        result = await self.collection.delete_one({"_id": oid})
        return result.deleted_count > 0

    async def delete_by_recruiter(self, recruiter_id: str) -> int:
        result = await self.collection.delete_many({"recruiter_id": recruiter_id})
        return result.deleted_count
