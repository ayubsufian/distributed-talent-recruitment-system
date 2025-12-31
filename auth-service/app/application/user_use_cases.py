from app.application.interfaces.repository import IUserRepository
from app.application.interfaces.messenger import IIdentityEventPublisher


class DeleteUserAccountUseCase:
    def __init__(self, repo: IUserRepository, messenger: IIdentityEventPublisher):
        self.repo = repo
        self.messenger = messenger

    async def execute(self, user_id: str) -> bool:
        """
        Deletes the user from the database and triggers the user.deleted event
        for cascading cleanup in other microservices.
        """
        # 1. Check if user exists
        user = await self.repo.get_by_id(user_id)
        if not user:
            return False

        # 2. Delete from Repository
        is_deleted = await self.repo.delete(user_id)

        # 3. Publish Event if deletion was successful
        if is_deleted:
            # This satisfies the requirement: "Cascading delete of user's jobs/apps/notifications"
            await self.messenger.publish_user_deleted(user_id)

        return is_deleted
