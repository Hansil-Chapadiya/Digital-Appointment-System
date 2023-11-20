# app/router.py
from fastapi import APIRouter, HTTPException
from Controller.admin_controller import AdminController
from Model.admin_model import Admin
from fastapi.responses import JSONResponse
from typing import List

AdminRouter = APIRouter()

@AdminRouter.get("/admin/", response_model=List[Admin])
async def read_admins():
    admins = await AdminController.get_admins()
    return admins

@AdminRouter.get("/admin/{admin_id}", response_model=Admin)
async def read_admin(admin_id: str):
    try:
        admin = await AdminController.admin_login(admin_id)
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
async def create_admin(admin_: Admin):
    return AdminController.create_admin(admin_)

@AdminRouter.get("/admin/login/{admin_id}", response_model=Admin)
async def admin_login(admin_id: str):
    try:
        admin = await AdminController.admin_login(admin_id)
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