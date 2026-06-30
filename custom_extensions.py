"""Management of custom file extensions and categories."""

import json
from pathlib import Path
from typing import Dict, List, Optional


class CustomExtensionsManager:
    """Manages user-defined custom extensions and categories."""

    # Use application data directory in user's home
    DATA_DIR = Path.home() / ".gestor_carpetas"
    CONFIG_FILE = DATA_DIR / "custom_extensions.json"

    def __init__(self):
        """Initialize the manager and ensure data directory exists."""
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.custom_extensions: Dict[str, List[str]] = {}
        self.load_extensions()

    def load_extensions(self) -> bool:
        """
        Load custom extensions from config file.
        
        Returns:
            True if loaded successfully, False otherwise.
        """
        try:
            if self.CONFIG_FILE.exists():
                with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                    self.custom_extensions = json.load(f)
                return True
            return False
        except Exception as e:
            print(f"Error loading extensions: {e}")
            return False

    def save_extensions(self) -> bool:
        """
        Save custom extensions to config file.
        
        Returns:
            True if saved successfully, False otherwise.
        """
        try:
            self.DATA_DIR.mkdir(parents=True, exist_ok=True)
            with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.custom_extensions, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving extensions: {e}")
            return False

    def add_extension(self, category: str, extensions: List[str]) -> bool:
        """
        Add or update a custom category with extensions.
        
        Args:
            category: Category name (folder name).
            extensions: List of file extensions (e.g., ['.psd', '.ai']).
            
        Returns:
            True if successful.
        """
        # Normalize extensions (ensure they start with a dot)
        normalized = []
        for ext in extensions:
            if ext and not ext.startswith("."):
                normalized.append("." + ext.lower())
            elif ext:
                normalized.append(ext.lower())
        
        if category and normalized:
            self.custom_extensions[category] = normalized
            self.save_extensions()
            return True
        return False

    def remove_category(self, category: str) -> bool:
        """
        Remove a custom category.
        
        Args:
            category: Category name to remove.
            
        Returns:
            True if removed, False if not found.
        """
        if category in self.custom_extensions:
            del self.custom_extensions[category]
            self.save_extensions()
            return True
        return False

    def get_all_categories(self) -> Dict[str, List[str]]:
        """
        Get all custom categories and their extensions.
        
        Returns:
            Dictionary of categories and extensions.
        """
        return self.custom_extensions.copy()

    def get_extensions_for_category(self, category: str) -> List[str]:
        """
        Get extensions for a specific category.
        
        Args:
            category: Category name.
            
        Returns:
            List of extensions, empty list if category not found.
        """
        return self.custom_extensions.get(category, [])

    def find_category_by_extension(self, extension: str) -> Optional[str]:
        """
        Find which custom category an extension belongs to.
        
        Args:
            extension: File extension (e.g., '.psd').
            
        Returns:
            Category name or None if not found.
        """
        ext = extension.lower() if extension.startswith(".") else f".{extension}".lower()
        
        for category, extensions in self.custom_extensions.items():
            if ext in extensions:
                return category
        return None

    def validate_category_name(self, name: str) -> bool:
        """
        Validate if category name is suitable for folder creation.
        
        Args:
            name: Category name to validate.
            
        Returns:
            True if valid.
        """
        # Invalid characters for folder names on Windows
        invalid_chars = '<>:"|?*'
        return name and not any(char in name for char in invalid_chars)

    def rename_category(self, old_name: str, new_name: str) -> bool:
        """
        Rename a custom category.
        
        Args:
            old_name: Current category name.
            new_name: New category name.
            
        Returns:
            True if successful.
        """
        if old_name in self.custom_extensions and self.validate_category_name(new_name):
            extensions = self.custom_extensions.pop(old_name)
            self.custom_extensions[new_name] = extensions
            self.save_extensions()
            return True
        return False


# Singleton instance and utility functions
_manager_instance = None


def get_extensions_manager() -> CustomExtensionsManager:
    """Get or create the singleton CustomExtensionsManager instance."""
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = CustomExtensionsManager()
    return _manager_instance


def load_all_extensions() -> Dict[str, List[str]]:
    """
    Load all extensions (predefined + custom).
    
    Returns:
        Dictionary with all categories and their extensions.
    """
    from constants import EXTENSIONES_PREDEFINIDAS
    
    manager = get_extensions_manager()
    custom_extensions = manager.get_all_categories()
    
    # Create a copy of predefined extensions
    all_extensions = EXTENSIONES_PREDEFINIDAS.copy()
    
    # Identify all extensions defined in custom categories
    custom_ext_set = {ext for exts in custom_extensions.values() for ext in exts}
    
    # Remove these extensions from any predefined categories
    for category in all_extensions:
        all_extensions[category] = [ext for ext in all_extensions[category] if ext not in custom_ext_set]
    
    # Add custom categories last to ensure they take priority
    all_extensions.update(custom_extensions)
    
    return all_extensions
