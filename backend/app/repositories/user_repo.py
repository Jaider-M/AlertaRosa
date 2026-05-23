from typing import Optional
from app.repositories.base import BaseRepository
from app.models.auth import User, UserRole, SpecialistProfile 
from app.models.patient import PatientDemographics
from app.schemas.user import UserCreate, UserUpdate
from app.security import get_password_hash 

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    async def get_by_username(self, username: str) -> Optional[User]:
        return await self.model.find_one(self.model.username == username)
        
    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.model.find_one(self.model.email == email)

    async def create(self, obj_in: UserCreate) -> User:
        db_user = User(
            username=obj_in.username,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            role=obj_in.role
        )
        await db_user.insert()

        try:
            if obj_in.role == UserRole.PATIENT:
                patient_profile = PatientDemographics(
                    user=db_user, 
                    medical_record_number=obj_in.medical_record_number,
                    full_name=obj_in.full_name,
                    date_of_birth=obj_in.date_of_birth,
                    phone=obj_in.phone,
                    address=obj_in.address,
                    prioridad="Baja" 
                )
                await patient_profile.insert()

            elif obj_in.role == UserRole.SPECIALIST:
                specialist_profile = SpecialistProfile(
                    user=db_user,
                    nombre_completo=obj_in.nombre_completo,
                    especialidad=obj_in.especialidad,
                    registro_medico=obj_in.registro_medico
                )
                await specialist_profile.insert()
            
            return db_user

        except Exception as e:
            await db_user.delete()
            raise e

user_repo = UserRepository(User)