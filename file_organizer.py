"""File organization logic for GestorCarpetas."""

import shutil
from pathlib import Path
from typing import Callable, Optional
from constants import EXTENSIONES, OTROS_FOLDER, PRESET_STRUCTURES


class FileOrganizer:
    """Handles file organization logic."""

    def __init__(self, callback: Optional[Callable[[str], None]] = None):
        """
        Initialize FileOrganizer.
        
        Args:
            callback: Optional callback function to report status messages.
        """
        self.callback = callback or (lambda x: None)
        self.ruta: Optional[Path] = None

    def set_folder(self, folder_path: str) -> bool:
        """
        Set the target folder for organization.
        
        Args:
            folder_path: Path to the folder to organize.
            
        Returns:
            True if folder exists and is valid, False otherwise.
        """
        self.ruta = Path(folder_path)
        if not self.ruta.exists():
            self.callback("❌ La carpeta no existe.")
            return False
        if not self.ruta.is_dir():
            self.callback("❌ La ruta no es una carpeta.")
            return False
        self.callback(f"✅ Carpeta seleccionada: {self.ruta}")
        return True

    def create_category_folders(self) -> bool:
        """
        Create category folders.
        
        Returns:
            True if successful, False otherwise.
        """
        if not self.ruta:
            self.callback("❌ No hay carpeta seleccionada.")
            return False

        try:
            for categoria in EXTENSIONES.keys():
                folder = self.ruta / categoria
                folder.mkdir(exist_ok=True)
            
            (self.ruta / OTROS_FOLDER).mkdir(exist_ok=True)
            self.callback("✅ Carpetas de categoría creadas.")
            return True
        except Exception as e:
            self.callback(f"❌ Error al crear carpetas: {str(e)}")
            return False

    def organize_files(self) -> dict:
        """
        Organize files into category folders.
        
        Returns:
            Dictionary with statistics: {
                'moved': int,
                'errors': list,
                'summary': str
            }
        """
        if not self.ruta:
            self.callback("❌ No hay carpeta seleccionada.")
            return {"moved": 0, "errors": [], "summary": "No hay carpeta seleccionada"}

        stats = {"moved": 0, "errors": []}

        try:
            # Create category folders first
            self.create_category_folders()

            # Organize files
            files = [f for f in self.ruta.iterdir() if f.is_file()]
            
            for archivo in files:
                try:
                    extension = archivo.suffix.lower()
                    destino = OTROS_FOLDER

                    # Find matching category
                    for categoria, extensiones in EXTENSIONES.items():
                        if extension in extensiones:
                            destino = categoria
                            break

                    # Move file
                    destino_path = self.ruta / destino / archivo.name
                    shutil.move(str(archivo), str(destino_path))
                    stats["moved"] += 1
                    self.callback(f"Movido: {archivo.name} → {destino}/")
                except Exception as e:
                    error_msg = f"Error al mover {archivo.name}: {str(e)}"
                    stats["errors"].append(error_msg)
                    self.callback(f"⚠️ {error_msg}")

            # Generate summary
            summary = f"✅ Operación completada: {stats['moved']} archivos movidos"
            if stats["errors"]:
                summary += f" ({len(stats['errors'])} errores)"
            stats["summary"] = summary
            self.callback(summary)
            return stats

        except Exception as e:
            error_msg = f"❌ Error durante la organización: {str(e)}"
            self.callback(error_msg)
            return {
                "moved": 0,
                "errors": [error_msg],
                "summary": error_msg,
            }

    def create_folder_structure(self, preset_name: str = None, folders: list[str] = None) -> bool:
        """
        Create a preset or custom folder structure in the selected directory.
        """
        if not self.ruta:
            self.callback("❌ No hay carpeta seleccionada.")
            return False

        try:
            if folders is not None:
                structure_folders = folders
            elif preset_name and preset_name in PRESET_STRUCTURES:
                structure_folders = PRESET_STRUCTURES[preset_name]
            else:
                structure_folders = list(EXTENSIONES.keys())

            for folder_name in structure_folders:
                (self.ruta / folder_name).mkdir(parents=True, exist_ok=True)

            (self.ruta / OTROS_FOLDER).mkdir(exist_ok=True)
            preset_label = preset_name or "Básico"
            mensaje = f"✅ Estructura '{preset_label}' creada."
            self.callback(mensaje)
            return True
        except Exception as e:
            self.callback(f"❌ Error al crear estructura: {str(e)}")
            return False

    def delete_folder_structure(self, preset_name: str = None) -> bool:
        """
        Delete preset or category folders in the selected directory.
        Only empty folders will be deleted to prevent accidental data loss.
        """
        if not self.ruta:
            self.callback("❌ No hay carpeta seleccionada.")
            return False

        try:
            if preset_name and preset_name in PRESET_STRUCTURES:
                folders_to_remove = PRESET_STRUCTURES[preset_name] + [OTROS_FOLDER]
            else:
                folders_to_remove = list(EXTENSIONES.keys()) + [OTROS_FOLDER]

            deleted_count = 0
            for folder_name in folders_to_remove:
                folder = self.ruta / folder_name
                if folder.exists() and folder.is_dir():
                    try:
                        folder.rmdir()  # Solo elimina si está vacía
                        self.callback(f"🗑️ Carpeta vacía eliminada: {folder_name}")
                        deleted_count += 1
                    except OSError:
                        self.callback(f"⚠️ Carpeta '{folder_name}' no eliminada porque contiene archivos.")

            self.callback(f"✅ Eliminación completada ({deleted_count} carpetas eliminadas).")
            return True
        except Exception as e:
            self.callback(f"❌ Error al eliminar carpetas: {str(e)}")
            return False

    def get_folder_structure(self) -> Optional[dict]:
        """
        Get the folder structure tree.
        
        Returns:
            Dictionary representing the folder tree, or None if no folder selected.
        """
        if not self.ruta or not self.ruta.exists():
            return None

        def build_tree(path: Path, prefix: str = "") -> dict:
            """Recursively build folder structure."""
            tree = {
                "name": path.name or str(path),
                "type": "folder",
                "path": str(path),
                "children": [],
                "count": 0,
            }

            try:
                items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
                
                for item in items:
                    if item.is_dir():
                        subtree = build_tree(item, prefix + "  ")
                        tree["children"].append(subtree)
                        tree["count"] += subtree["count"] + 1
                    elif item.is_file():
                        tree["children"].append({
                            "name": item.name,
                            "type": "file",
                            "path": str(item),
                            "size": item.stat().st_size,
                        })
                        tree["count"] += 1
            except PermissionError:
                tree["error"] = "Permiso denegado"

            return tree

        return build_tree(self.ruta)
