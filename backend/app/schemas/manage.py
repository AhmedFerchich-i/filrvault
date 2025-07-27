# app/schemas/explore.py
from pydantic import BaseModel
from typing import List

class FileInfo(BaseModel):
    name: str
    path: str
    is_file: bool
    size: int

class DirectoryListingResponse(BaseModel):
    files: List[FileInfo]
