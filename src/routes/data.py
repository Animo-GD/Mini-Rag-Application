from fastapi import APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from utilis.config import get_settings,Setting
from controllers import DataController,ProjectController
from models import ResponseSignal
import os
import aiofiles

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str,file:UploadFile,app_settings:Setting = Depends(get_settings)):
    # Validate Files
    is_valid,return_msg = DataController().validate_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "msg":return_msg
                }
              )
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path = os.path.join(project_dir_path,file.filename)

    async with aiofiles.open(file_path,"wb") as f:
        while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
            await f.write(chunk)
    
    return JSONResponse(
            content={
                "msg":ResponseSignal.FILE_UPLOADED_SUCCESS
                }
              )