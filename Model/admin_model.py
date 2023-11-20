from pydantic import BaseModel, Field, validator
from bson import ObjectId
from typing import Optional

class Admin(BaseModel):
    id: str = Field(..., alias='_id', description='The ID of the admin.')
    a_name: str
    a_email: str
    a_mobile: str
    a_password: str
    a_profile_image: Optional[str] = None

    @validator("id")
    def validate_id(cls, value):
        if not ObjectId.is_valid(str(value)):
            raise ValueError('Invalid ObjectId')
        return str(value)
