from fastapi import FastAPI,APIRouter,Depends
from utilis.config import get_settings,Setting
import os

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"]
)

@base_router.get("/")
async def home(app_setting:Setting = Depends(get_settings)):
    app_setting = get_settings()
    app_name = app_setting.APP_NAME
    app_version = app_setting.APP_VERSION
    return {
        "app_name":app_name,
        "app_version":app_version
        }

