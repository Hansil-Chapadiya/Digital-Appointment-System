# app/controllers/item_controller.py
from typing import List, Dict
from fastapi import HTTPException, Body, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from jwt import encode as jwt_encode
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from config import params
from Model.admin_model import Admin
from Controller.db_init import get_database
from Controller.check_admin_password import verify_password


class AdminController:
    admin_db = []

    @classmethod
    async def get_collection(cls) -> AsyncIOMotorDatabase:
        database = await get_database()
        return database

    @classmethod
    async def get_admins(cls) -> List[Admin]:
        collection = await cls.get_collection()
        admin_list = await collection["Admin_hack"].find({}).to_list(length=None)  # type: ignore

        # Convert ObjectId fields to strings
        for admin in admin_list:
            admin["_id"] = str(admin["_id"])

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
                admin["_id"] = str(admin["_id"])
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
    async def admin_login(cls, data: dict = Body(...)) -> JSONResponse:
        try:
            a_email = data.get("a_email")
            a_password = data.get("a_password")
            collection = await cls.get_collection()
            admin = collection["Admin_hack"]

            email_found = await admin.find_one({"a_email": a_email})
            if email_found:
                password_matched = verify_password(
                    a_password, email_found["a_password"]
                )
                if password_matched:
                    token = jwt_encode(
                        {
                            "email": email_found["a_email"],
                            "exp": datetime.utcnow() + timedelta(minutes=2880),
                        },
                        params["API_KEY"],
                        algorithm="HS256",
                    )
                    return JSONResponse(content={"status": True, "token": token})
                else:
                    raise HTTPException(status_code=401, detail="Incorrect password")
            else:
                raise HTTPException(status_code=404, detail="Admin not found")
        except IndexError:
            raise HTTPException(status_code=404, detail="Admin not found")
