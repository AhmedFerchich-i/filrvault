from pydantic import BaseModel, Field
from typing import Optional

# --- 1. Init Upload Request ---
class UploadInitRequest(BaseModel):
    upload_id: str = Field(..., description="Unique upload session ID")
    filename: str = Field(..., description="Name of the file being uploaded")
    total_chunks: Optional[int] = Field(None, description="Number of chunks if chunked upload")
    subdirectory: Optional[str] = Field(None, description="Optional subdirectory")

# --- 1. Init Upload Response ---
class UploadInitResponse(BaseModel):
    message: str
    upload_id: Optional[str] = None

# --- 2. Chunk Upload Request ---
class UploadChunkRequest(BaseModel):
    upload_id: str = Field(..., description="Upload session ID")
    chunk_index: int = Field(..., ge=0, description="Index of this chunk, zero-based")
    subdirectory: Optional[str] = Field(None, description="Optional subdirectory")
    chunk_checksum: Optional[str] = Field(None, description="SHA-256 checksum of the chunk")

# --- 3. Assemble Request ---
class UploadAssembleRequest(BaseModel):
    upload_id: str = Field(..., description="Upload session ID")
    filename: str = Field(..., description="Final filename")
    total_chunks: int = Field(..., gt=0, description="Total chunks expected")
    final_checksum: Optional[str] = Field(None, description="SHA-256 checksum of the final file")
    subdirectory: Optional[str] = Field(None, description="Optional subdirectory")


