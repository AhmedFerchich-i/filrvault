from pathlib import Path
from fastapi import HTTPException

def secure_path(base: Path, target: str) -> Path:
    final_path = (base / target).resolve()
    if not str(final_path).startswith(str(base.resolve())):
        raise HTTPException(status_code=403, detail="Access to this path is forbidden")
    return final_path
