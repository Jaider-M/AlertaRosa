from typing import Generic, TypeVar, Type, Optional, List, Any, Union, Dict
from beanie import Document, PydanticObjectId
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=Document)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, id: Union[PydanticObjectId, str, Any]) -> Optional[ModelType]:
        return await self.model.get(id)

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return await self.model.find_all().skip(skip).limit(limit).to_list()

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        return await db_obj.insert()

    async def update(
        self, 
        db_obj: ModelType, 
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        update_data = {k: v for k, v in update_data.items() if k != "id"}
        
        if update_data:
            await db_obj.update({"$set": update_data})
            
        return await self.get(db_obj.id)

    async def remove(self, id: Union[PydanticObjectId, str, Any]) -> Optional[ModelType]:
        """Elimina un documento por su ID y lo retorna."""
        obj = await self.get(id)
        if obj:
            await obj.delete()
        return obj