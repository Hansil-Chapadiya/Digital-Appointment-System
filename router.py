# app/router.py
from fastapi import APIRouter
from Controller.admin_controller import AdminController
from Model.admin_model import Admin
from typing import List

AdminRouter = APIRouter()

@AdminRouter.get("/admin/", response_model=List[Admin])
async def read_items():
    return AdminController.get_admins()

@AdminRouter.get("/admin/{admin_id}", response_model=Admin)
async def read_item(admin_id: int):
    return AdminController.get_admin(admin_id)

@AdminRouter.post("/admin/create", response_model=Admin)
async def create_item(admin_: Admin):
    return AdminController.create_admin(admin_)
