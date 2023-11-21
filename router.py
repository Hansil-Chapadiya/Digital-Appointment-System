# app/router.py
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from typing import List
from Controller.check_admin_secrete_key import authenticate_api_key
from Controller.admin_authenticate import get_current_user
from Controller.admin_controller import AdminController
from Model.admin_model import Admin

AdminRouter = APIRouter()

admin_create_officer_route = APIRouter()
api_key_header = APIKeyHeader(name="API-Key")

@AdminRouter.get("/admin/", response_model=List[Admin])
# @get_current_user
async def read_admins():
    admins = await AdminController.get_admins()
    return admins

@AdminRouter.get("/admin/{admin_id}", response_model=Admin)
@get_current_user
async def read_admin(admin_id: str):
    try:
        admin = await AdminController.get_admin(admin_id)
        if admin:
            # Await the coroutine and convert it to a dictionary
            admin_data = admin  # Await the coroutine
            return JSONResponse(content=admin_data)
        else:
            raise HTTPException(status_code=404, detail="Admin not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@AdminRouter.post("/admin/create", response_model=Admin)
# @get_current_user
async def create_admin(admin_: Admin):
    return AdminController.create_admin(admin_)

@AdminRouter.post("/admin/login", response_model=Admin)
async def admin_login(data:dict = Body(...)):
    try:
        admin = await AdminController.admin_login(data)
        if admin:
            # Await the coroutine and convert it to a dictionary
            admin_data = admin  # Await the coroutine
            return admin_data
        else:
            raise HTTPException(status_code=404, detail="Admin not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))