from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError('Invalid ObjectId')
        return ObjectId(value)

class Admin(BaseModel):
    id: ObjectIdStr = Field(..., alias='_id')
    a_name: str
    a_email: str
    a_mobile: str
    a_password: str
    a_profile_image: Optional[str] = None
