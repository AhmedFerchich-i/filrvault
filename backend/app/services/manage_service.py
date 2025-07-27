
from fastapi import HTTPException
from typing import List
from core.config import settings
from schemas.manage import FileInfo
import shutil
from utils.path_utils import secure_path
from pathlib import Path


def list_subdirectories() -> List[str]:
    base_dir = settings.UPLOAD_DIR
    if not base_dir.exists() or not base_dir.is_dir():
        raise HTTPException(status_code=500, detail="Base upload directory does not exist.")

    return [p.name for p in base_dir.iterdir() if p.is_dir()]

def list_files(path: str) -> List[FileInfo]:
    base_dir = settings.UPLOAD_DIR.resolve()
    target_dir = (base_dir / path).resolve()

    if not str(target_dir).startswith(str(base_dir)):
        raise HTTPException(status_code=403, detail="Access to this path is forbidden.")

    if not target_dir.exists() or not target_dir.is_dir():
        raise HTTPException(status_code=404, detail="Directory not found.")

    files = []
    for item in target_dir.iterdir():
        files.append(
            FileInfo(
                name=item.name,
                path=str(item.relative_to(base_dir)),
                is_file=item.is_file(),
                size=item.stat().st_size,
            )
        )
    return files








UPLOAD_ROOT = settings.UPLOAD_DIR

def delete_file(relative_path: str):
    file_path = secure_path(UPLOAD_ROOT, relative_path)
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    file_path.unlink()

def delete_directory(relative_path: str):
    dir_path = secure_path(UPLOAD_ROOT, relative_path)
    if not dir_path.exists() or not dir_path.is_dir():
        raise HTTPException(status_code=404, detail="Directory not found")
    shutil.rmtree(dir_path)


def get_file_path(relative_path: str) -> Path:
    file_path = secure_path(settings.UPLOAD_DIR, relative_path)
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return file_path