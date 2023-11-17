from pydantic import BaseModel
from typing import Optional


class Admin(BaseModel):
    a_name: str
    a_email:str
    a_mobile: str
    a_password: str
    a_profile_image:Optional[str] = None
