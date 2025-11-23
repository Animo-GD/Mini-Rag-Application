from fastapi import APIRouter,Depends,UploadFile,status,Request
from fastapi.responses import JSONResponse
from utilis.config import get_settings,Setting
from controllers import DataController,ProjectController,ProcessController
from models import ResponseSignal
from routes.schemes.data import ProccessRequest
from models.ProjectModel import ProjectModel
from models.db_schemes import DataChunk,Asset
from models.ChunkModel import ChunkModel
from models.AssetModel import AssetModel
from models.enums import AssetTypeEnum
import aiofiles
import logging
import os

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(request:Request,project_id:str,file:UploadFile,app_settings:Setting = Depends(get_settings)):

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

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
    file_path,file_id = data_ctrl.generate_unique_filepath(
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
    # Store the assets into database
    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)
    asset_resource = Asset(
        asset_project_id=project.id,
        asset_type=AssetTypeEnum.FILE.value,
        asset_name=file_id,
        asset_size=os.path.getsize(file_path)
    )
    asset_record = await asset_model.create_asset(asset=asset_resource)
    return JSONResponse(
            content={
                "msg":ResponseSignal.FILE_UPLOADED_SUCCESS.value,
                "file_id":str(asset_record.id)
                }
              )

@data_router.post("/process/{project_id}")
async def process_endpoint(request:Request,project_id:str,process_request:ProccessRequest):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset
    process_controller = ProcessController(project_id=project_id)
    chunk_model =  await ChunkModel.create_instance(db_client=request.app.db_client)
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

    


    file_content = process_controller.get_file_content(file_id=file_id)

    file_chunks = process_controller.process_file_content(file_content=file_content,file_id=file_id
                                                           ,chunk_size=chunk_size,overlap_size=overlap_size)
    
    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":ResponseSignal.PROCESSING_FAILED
            }
        )
    
    file_chunks_records = [
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=i+1,
            chunk_project_id=project.id
        )
        for i,chunk in enumerate(file_chunks)
    ]
    if do_reset==1:
        _ = await chunk_model.delete_chunks_by_project_id(project_id=project.id)

    no_records = await chunk_model.insert_many_chunks(chunks=file_chunks_records)
    return JSONResponse(
        content={
            "signal":ResponseSignal.PROCESSING_SUCCESS.value,
            "inserted_chunks":no_records
        }
    )
