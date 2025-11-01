"""
File operation utilities for workflow system
"""

import json
import shutil
from pathlib import Path
from typing import Any, Dict, Optional


class FileUtils:
    """Utilities for file operations"""

    @staticmethod
    def ensure_dir(path: str) -> Path:
        """Ensure directory exists"""
        dir_path = Path(path)
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path

    @staticmethod
    def read_file(file_path: str) -> str:
        """Read entire file as string"""
        return Path(file_path).read_text(encoding='utf-8')

    @staticmethod
    def write_file(file_path: str, content: str) -> None:
        """Write content to file"""
        path = Path(file_path)
        FileUtils.ensure_dir(path.parent)
        path.write_text(content, encoding='utf-8')

    @staticmethod
    def read_json(file_path: str) -> Dict[str, Any]:
        """Read JSON file"""
        return json.loads(Path(file_path).read_text(encoding='utf-8'))

    @staticmethod
    def write_json(file_path: str, data: Dict[str, Any], indent: int = 2) -> None:
        """Write JSON file"""
        path = Path(file_path)
        FileUtils.ensure_dir(path.parent)
        path.write_text(
            json.dumps(data, indent=indent, ensure_ascii=False),
            encoding='utf-8'
        )

    @staticmethod
    def append_file(file_path: str, content: str) -> None:
        """Append content to file"""
        path = Path(file_path)
        FileUtils.ensure_dir(path.parent)
        with open(path, 'a', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def copy_file(src: str, dst: str) -> None:
        """Copy file from src to dst"""
        src_path = Path(src)
        dst_path = Path(dst)
        FileUtils.ensure_dir(dst_path.parent)
        shutil.copy2(src_path, dst_path)

    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Check if file exists"""
        return Path(file_path).exists()

    @staticmethod
    def dir_exists(dir_path: str) -> bool:
        """Check if directory exists"""
        return Path(dir_path).is_dir()

    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Get file size in bytes"""
        return Path(file_path).stat().st_size

    @staticmethod
    def delete_file(file_path: str) -> None:
        """Delete file"""
        Path(file_path).unlink(missing_ok=True)

    @staticmethod
    def delete_dir(dir_path: str) -> None:
        """Delete directory recursively"""
        shutil.rmtree(dir_path, ignore_errors=True)

    @staticmethod
    def list_files(dir_path: str, pattern: str = '*') -> list:
        """List files in directory matching pattern"""
        return list(Path(dir_path).glob(pattern))

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """Get file extension"""
        return Path(file_path).suffix

    @staticmethod
    def get_file_name(file_path: str) -> str:
        """Get file name without extension"""
        return Path(file_path).stem
