from pathlib import Path
import shutil

def safe_write_file(file_path: Path, data: bytes):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(data)

def cleanup_directory(path: Path):
    if path.exists() and path.is_dir():
        shutil.rmtree(path)
