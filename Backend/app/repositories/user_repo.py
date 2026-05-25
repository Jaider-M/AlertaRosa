from app.core.security import get_password_hash
from typing import Optional
from app.repositories.base import BaseRepository
from app.models.auth import User, UserRole
from app.schemas.user import UserCreate, UserUpdate

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    async def get_by_username(self, username: str) -> Optional[User]:
        return await self.model.find_one(self.model.username == username)
        
    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.model.find_one(self.model.email == email)

    async def create(self, obj_in: UserCreate) -> User:
        # Creamos la instancia del documento
        db_user = User(
            username=obj_in.username,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            role=obj_in.role
        )
        # Persistimos solo el usuario
        await db_user.insert()
        return db_user

user_repo = UserRepository(User)