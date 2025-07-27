from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from schemas.upload import (
    UploadInitRequest,
    UploadInitResponse,
    UploadChunkRequest,
    UploadAssembleRequest,
)
from services import upload_service

router = APIRouter()


# ========== 1. INIT UPLOAD ==========
@router.post("/init", response_model=UploadInitResponse)
def init_upload(request: UploadInitRequest):
    return upload_service.init_upload(request)


# ========== 2. CHUNK UPLOAD ==========
@router.post("/chunk")
async def upload_chunk(
    request: UploadChunkRequest = Form(...),
    chunk: UploadFile = File(...)
):
    return await upload_service.upload_chunk(request, chunk)


# ========== 3. ASSEMBLE CHUNKS ==========
@router.post("/assemble")
def assemble_chunks(request: UploadAssembleRequest):
    return upload_service.assemble_chunks(request)


# ========== 4. SIMPLE ONE-SHOT FILE UPLOAD ==========
@router.post("/file", response_model=UploadInitResponse)
async def upload_file(
    file: UploadFile = File(...),
    subdirectory: str = Form(None)
):
    return await upload_service.upload_file(file, subdirectory)
