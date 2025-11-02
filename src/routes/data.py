from fastapi import APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from utilis.config import get_settings,Setting
from controllers import DataController,ProjectController
from models import ResponseSignal
import aiofiles
import logging

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str,file:UploadFile,app_settings:Setting = Depends(get_settings)):
    data_ctrl=DataController()
    # Validate Files
    is_valid,return_msg = data_ctrl.validate_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "msg":return_msg
                }
              )
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path = data_ctrl.generate_unique_filename(
        orig_file_name=file.filename,
        project_id=project_id
    )
    try:
        async with aiofiles.open(file_path,"wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error while uploading file {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "msg":ResponseSignal.FILE_UPLOADED_FALIED.value
                }
              )
    
    return JSONResponse(
            content={
                "msg":ResponseSignal.FILE_UPLOADED_SUCCESS.value
                }
              )