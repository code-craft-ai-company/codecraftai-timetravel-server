import os
import shutil
import datetime
from typing import List
from pathlib import Path

from .backend_abc import TraceStorageBackend

class FilesystemTraceStorage(TraceStorageBackend):
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir = self.base_dir / "temp"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.final_dir = self.base_dir / "final"
        self.final_dir.mkdir(parents=True, exist_ok=True)

    def write(self, data: bytes, session_id: str) -> str:
        temp_path = self.temp_dir / f"{session_id}.trace.tmp"
        with open(temp_path, "wb") as f:
            f.write(data)
        return str(temp_path)

    def append(self, reference: str, data: bytes) -> bool:
        ref_path = Path(reference)
        if not ref_path.exists():
            return False
        with open(ref_path, "ab") as f:
            f.write(data)
        return True

    def finalize(self, reference: str) -> str:
        ref_path = Path(reference)
        if not ref_path.exists():
            raise FileNotFoundError(f"Reference not found: {reference}")

        final_filename = ref_path.name.replace(".tmp", "")
        final_path = self.final_dir / final_filename

        # Atomic rename
        ref_path.rename(final_path)
        return str(final_path)

    def read(self, reference: str) -> bytes:
        ref_path = Path(reference)
        if not ref_path.exists():
            raise FileNotFoundError(f"Reference not found: {reference}")
        with open(ref_path, "rb") as f:
            return f.read()

    def list_references(self) -> List[str]:
        refs = []
        for p in self.final_dir.rglob("*.trace"):
            if p.is_file():
                refs.append(str(p))
        return refs

    def delete(self, reference: str) -> bool:
        ref_path = Path(reference)
        if ref_path.exists() and ref_path.is_file():
            ref_path.unlink()
            return True
        return False

    def exists(self, reference: str) -> bool:
        return Path(reference).exists()

    def list_expired(self, cutoff_time: datetime.datetime) -> List[str]:
        refs = []
        for p in self.final_dir.rglob("*.trace"):
            if p.is_file():
                mtime = datetime.datetime.fromtimestamp(p.stat().st_mtime)
                if mtime < cutoff_time:
                    refs.append(str(p))
        return refs
