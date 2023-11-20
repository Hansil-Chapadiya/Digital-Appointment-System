# app/controllers/item_controller.py
from typing import List
from fastapi import HTTPException
from bson import ObjectId
from Model.admin_model import Admin
from Controller.db_init import get_database

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

   # AdminController.admin_login method
    @classmethod
    async def admin_login(cls, admin_id: str):
        try:
            collection = await get_database()
            admin = await collection["Admin_hack"].find_one({"_id": ObjectId(admin_id)})

            if admin:
                # Convert ObjectId to string before returning
                admin['_id'] = str(admin['_id'])
                return admin
            else:
                raise HTTPException(status_code=404, detail="Admin not found")
        except IndexError:
            raise HTTPException(status_code=404, detail="Admin not found")
