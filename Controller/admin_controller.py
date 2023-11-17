# app/controllers/item_controller.py
from typing import List
from fastapi import HTTPException
from Model.admin_model import Admin

class AdminController:
    admin_db = []

    @classmethod
    def get_admins(cls) -> List[Admin]:
        return cls.admin_db

    @classmethod
    def get_admin(cls, admin_id: int) -> Admin:
        try:
            return cls.admin_db[admin_id]
        except IndexError:
            raise HTTPException(status_code=404, detail="Admin not found")

    @classmethod
    def create_admin(cls, admin_: Admin) -> Admin:
        cls.admin_db.append(admin_)
        return admin_