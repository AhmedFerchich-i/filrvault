import hashlib
from pathlib import Path

def calculate_sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def calculate_sha256_file(file_path: Path) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()
