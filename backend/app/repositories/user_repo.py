from typing import Optional
from app.repositories.base import BaseRepository
from app.models.auth import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    async def get_by_username(self, username: str) -> Optional[User]:
        return await self.model.find_one(self.model.username == username)
        
    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.model.find_one(self.model.email == email)

    async def create(self, obj_in: UserCreate) -> User:
        user_data = obj_in.model_dump()
        plain_password = user_data.pop("password")
        user_data["hashed_password"] = get_password_hash(plain_password)
        db_obj = User(**user_data)
        
        return await db_obj.insert()

user_repo = UserRepository(User)