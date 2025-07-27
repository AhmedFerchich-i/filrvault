from pathlib import Path
from fastapi import HTTPException, UploadFile
from typing import Optional

from core.config import settings
from schemas.upload import (
    UploadInitRequest,
    UploadInitResponse,
    UploadChunkRequest,
    UploadAssembleRequest,
)
from utils.file_utils import safe_write_file, cleanup_directory
from utils.checksum_utils import calculate_sha256_bytes, calculate_sha256_file
from utils.path_utils import secure_path  # import the secure_path helper


def init_upload(request: UploadInitRequest) -> UploadInitResponse:
    """
    Prepare the temporary chunk folder for the upload session.
    """
    # Securely resolve the upload directory path
    upload_dir = secure_path(settings.UPLOAD_DIR, (request.subdirectory or "") + f"/{request.upload_id}")
    upload_dir.mkdir(parents=True, exist_ok=True)

    return UploadInitResponse(message="Upload session initialized", upload_id=request.upload_id)


async def upload_chunk(request: UploadChunkRequest, chunk: UploadFile):
    """
    Save a chunk file and optionally verify its checksum.
    """
    upload_dir = secure_path(settings.UPLOAD_DIR, (request.subdirectory or "") + f"/{request.upload_id}")
    if not upload_dir.exists():
        raise HTTPException(status_code=400, detail="Upload session not initialized.")

    chunk_path = upload_dir / f"chunk_{request.chunk_index}"
    content = await chunk.read()

    # Optional checksum verification
    if request.chunk_checksum:
        actual_checksum = calculate_sha256_bytes(content)
        if actual_checksum != request.chunk_checksum:
            raise HTTPException(status_code=400, detail="Chunk checksum mismatch.")

    safe_write_file(chunk_path, content)

    return {"message": f"Chunk {request.chunk_index} uploaded successfully."}


def assemble_chunks(request: UploadAssembleRequest):
    """
    Combine all chunks into the final file and validate its checksum.
    """
    upload_dir = secure_path(settings.UPLOAD_DIR, (request.subdirectory or "") + f"/{request.upload_id}")
    if not upload_dir.exists():
        raise HTTPException(status_code=404, detail="Upload session not found.")

    final_path = secure_path(settings.UPLOAD_DIR, (request.subdirectory or "") + f"/{request.filename}")

    with open(final_path, "wb") as outfile:
        for i in range(request.total_chunks):
            chunk_file = upload_dir / f"chunk_{i}"
            if not chunk_file.exists():
                raise HTTPException(status_code=400, detail=f"Missing chunk {i}.")
            with open(chunk_file, "rb") as cf:
                outfile.write(cf.read())

    # Optional final checksum validation
    if request.final_checksum:
        actual_checksum = calculate_sha256_file(final_path)
        if actual_checksum != request.final_checksum:
            final_path.unlink(missing_ok=True)
            raise HTTPException(status_code=400, detail="Final file checksum mismatch.")

    cleanup_directory(upload_dir)

    return {"message": f"File assembled and saved as {final_path}"}


async def upload_file(file: UploadFile, subdirectory: Optional[str] = None):
    """
    Handle a simple, one-shot file upload.
    """
    upload_dir = secure_path(settings.UPLOAD_DIR, subdirectory or "")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / file.filename
    content = await file.read()

    safe_write_file(file_path, content)

    return {"message": f"File '{file.filename}' uploaded successfully.", "file_path": str(file_path)}
