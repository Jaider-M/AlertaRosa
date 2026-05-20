from typing import Generic, TypeVar, Type, Optional, List, Any, Union, Dict
from beanie import Document, PydanticObjectId
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=Document)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, id: PydanticObjectId) -> Optional[ModelType]:
        return await self.model.get(id)

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return await self.model.find_all().skip(skip).limit(limit).to_list()

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        # Corregido: .dict() cambiado por .model_dump() de Pydantic v2
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        return await db_obj.insert()

    async def update(self, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        # Corregido: .dict() cambiado por .model_dump()
        obj_data = db_obj.model_dump()
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # Corregido: exclude_unset=True se mantiene dentro de model_dump()
            update_data = obj_in.model_dump(exclude_unset=True)
            
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        return await db_obj.save()

    async def remove(self, id: PydanticObjectId) -> Optional[ModelType]:
        obj = await self.model.get(id)
        if obj:
            await obj.delete()
        return obj