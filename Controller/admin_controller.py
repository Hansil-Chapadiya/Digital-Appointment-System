# app/controllers/item_controller.py
from typing import List, Dict
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from Model.admin_model import Admin
from Controller.db_init import get_database

class AdminController:
    admin_db = []
    @classmethod
    async def get_collection(cls) -> AsyncIOMotorDatabase:
        collection = await get_database()
        return collection

    @classmethod
    async def get_admins(cls) -> List[Admin]:
        collection = await cls.get_collection()
        admin_list = await collection['Admin_hack'].find({}).to_list(length=None) # type: ignore

        # Convert ObjectId fields to strings
        for admin in admin_list:
            admin['_id'] = str(admin['_id'])

        # Use the list of dictionaries to initialize a list of Admin models
        admins = [Admin(**admin) for admin in admin_list]

        return admins

    @classmethod
    async def get_admin(cls, admin_id: str) -> Admin:
        try:
            collection = await cls.get_collection()
            admin = await collection["Admin_hack"].find_one({"_id": ObjectId(admin_id)})

            if admin:
                # Convert ObjectId to string before returning
                admin['_id'] = str(admin['_id'])
                return admin
            else:
                raise HTTPException(status_code=404, detail="Admin not found")
        except IndexError:
            raise HTTPException(status_code=404, detail="Admin not found")

    @classmethod
    def create_admin(cls, admin_: Admin) -> Admin:
        cls.admin_db.append(admin_)
        return admin_

   # AdminController.admin_login method
    @classmethod
    async def admin_login(cls, admin_id: str) -> Admin:
        try:
            collection = await cls.get_collection()
            admin = await collection["Admin_hack"].find_one({"_id": ObjectId(admin_id)})

            if admin:
                # Convert ObjectId to string before returning
                admin['_id'] = str(admin['_id'])
                return admin
            else:
                raise HTTPException(status_code=404, detail="Admin not found")
        except IndexError:
            raise HTTPException(status_code=404, detail="Admin not found")
