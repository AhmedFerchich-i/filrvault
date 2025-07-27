from fastapi import APIRouter, Query
from typing import List
from schemas.manage import DirectoryListingResponse
from services import manage_service
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/subdirs", response_model=List[str])
def get_subdirectories():
    return manage_service.list_subdirectories()

@router.get("/files", response_model=DirectoryListingResponse)
def get_files(path: str = Query("")):
    files = manage_service.list_files(path)
    return DirectoryListingResponse(files=files)
@router.delete("/file")
def delete_file(path: str = Query(..., description="Relative path to file under upload dir")):
    manage_service.delete_file(path)
    return {"message": "File deleted successfully"}

@router.delete("/dir")
def delete_dir(path: str = Query(..., description="Relative path to directory under upload dir")):
    manage_service.delete_directory(path)
    return {"message": "Directory deleted successfully"}

@router.get("/download/file")
def download_file(path: str = Query(..., description="Relative path to file inside upload directory")):
    file_path = manage_service.get_file_path(path)
    return FileResponse(path=file_path, filename=file_path.name, media_type='application/octet-stream')