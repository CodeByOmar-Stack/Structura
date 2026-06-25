"""Utility functions for GestorCarpetas."""

import os
import shutil
from pathlib import Path
from typing import List, Tuple
from advanced_config import FILE_EMOJIS, IGNORED_FOLDERS


def get_file_icon(filename: str) -> str:
    """
    Get emoji icon for a file based on its extension.
    
    Args:
        filename: Name of the file.
        
    Returns:
        Emoji icon as string.
    """
    ext = Path(filename).suffix.lower()
    return FILE_EMOJIS.get(ext, FILE_EMOJIS.get("default", "📄"))


def get_human_readable_size(size_bytes: int) -> str:
    """
    Convert bytes to human-readable format.
    
    Args:
        size_bytes: Size in bytes.
        
    Returns:
        Formatted size string (e.g., "1.5 MB").
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def get_folder_statistics(folder_path: Path) -> dict:
    """
    Get statistics about folder contents.
    
    Args:
        folder_path: Path to folder.
        
    Returns:
        Dictionary with statistics.
    """
    stats = {
        "total_files": 0,
        "total_folders": 0,
        "total_size": 0,
        "extensions": {},
    }

    try:
        for item in folder_path.rglob("*"):
            if item.is_file():
                stats["total_files"] += 1
                stats["total_size"] += item.stat().st_size
                
                ext = item.suffix.lower()
                stats["extensions"][ext] = stats["extensions"].get(ext, 0) + 1
            elif item.is_dir():
                stats["total_folders"] += 1
    except PermissionError:
        pass

    return stats


def create_backup(folder_path: Path, backup_name: str = ".backup") -> Tuple[bool, str]:
    """
    Create a backup of the folder before organizing.
    
    Args:
        folder_path: Path to folder to backup.
        backup_name: Name of backup folder.
        
    Returns:
        Tuple (success, message).
    """
    try:
        backup_path = folder_path / backup_name
        if backup_path.exists():
            shutil.rmtree(backup_path)
        
        shutil.copytree(folder_path, backup_path, ignore=shutil.ignore_patterns(backup_name))
        return True, f"✅ Backup creado: {backup_path}"
    except Exception as e:
        return False, f"❌ Error al crear backup: {str(e)}"


def restore_from_backup(folder_path: Path, backup_name: str = ".backup") -> Tuple[bool, str]:
    """
    Restore folder from backup.
    
    Args:
        folder_path: Path to folder to restore.
        backup_name: Name of backup folder.
        
    Returns:
        Tuple (success, message).
    """
    backup_path = folder_path / backup_name
    if not backup_path.exists():
        return False, "❌ No se encontró backup para restaurar."

    try:
        # Remove current contents
        for item in folder_path.iterdir():
            if item.name != backup_name:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()

        # Restore from backup
        for item in backup_path.iterdir():
            dest = folder_path / item.name
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)

        return True, "✅ Carpeta restaurada desde backup"
    except Exception as e:
        return False, f"❌ Error al restaurar: {str(e)}"


def is_ignored_folder(folder_name: str) -> bool:
    """
    Check if folder should be ignored during scanning.
    
    Args:
        folder_name: Name of folder.
        
    Returns:
        True if folder should be ignored.
    """
    return folder_name in IGNORED_FOLDERS or folder_name.startswith(".")


def get_duplicate_files(folder_path: Path) -> dict:
    """
    Find duplicate files in folder.
    
    Args:
        folder_path: Path to folder.
        
    Returns:
        Dictionary mapping file hashes to file paths.
    """
    import hashlib
    
    duplicates = {}
    
    try:
        for file_path in folder_path.rglob("*"):
            if file_path.is_file() and file_path.stat().st_size > 0:
                # Calculate MD5 hash
                hash_md5 = hashlib.md5()
                with open(file_path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
                
                file_hash = hash_md5.hexdigest()
                if file_hash not in duplicates:
                    duplicates[file_hash] = []
                duplicates[file_hash].append(str(file_path))
    except Exception as e:
        print(f"Error scanning files: {e}")

    # Filter to only actual duplicates
    return {k: v for k, v in duplicates.items() if len(v) > 1}
