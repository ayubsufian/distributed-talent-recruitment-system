from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from app.domain.models import User
from app.application.interfaces.repository import IUserRepository


class MongoUserRepository(IUserRepository):

    def __init__(self, client: AsyncIOMotorClient, db_name: str):
        self.db = client[db_name]
        self.collection = self.db["users"]

    def _map_to_domain(self, user_doc: dict) -> User:
        if not user_doc:
            return None
        # Map MongoDB _id to Pydantic id
        user_doc["id"] = str(user_doc["_id"])
        return User(**user_doc)

    async def get_by_email(self, email: str) -> Optional[User]:
        user_doc = await self.collection.find_one({"email": email})
        return self._map_to_domain(user_doc)

    async def get_by_id(self, user_id: str) -> Optional[User]:
        try:
            oid = ObjectId(user_id)
        except Exception:
            return None
        user_doc = await self.collection.find_one({"_id": oid})
        return self._map_to_domain(user_doc)

    async def save(self, user: User) -> User:
        # Pydantic v2: use model_dump()
        user_dict = user.model_dump(exclude={"id"})

        if user.id:
            # Update existing
            await self.collection.update_one(
                {"_id": ObjectId(user.id)}, {"$set": user_dict}
            )
            return user
        else:
            # Insert new
            result = await self.collection.insert_one(user_dict)
            # Ensure the returned entity has the new ID as a string
            user.id = str(result.inserted_id)
            return user

    async def delete(self, user_id: str) -> bool:
        try:
            oid = ObjectId(user_id)
        except Exception:
            return False

        result = await self.collection.delete_one({"_id": oid})
        return result.deleted_count > 0
