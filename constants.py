"""Configuration and constants for GestorCarpetas."""

from pathlib import Path

# File extensions by category (predefined)
EXTENSIONES_PREDEFINIDAS = {
    "Imagenes": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg"],
    "Documentos": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".odt"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm", ".m4v"],
    "Musica": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".m4a"],
    "Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Codigo": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".go", ".rs"],
}

# Combined extensions (predefined + custom)
# Always reloaded from disk to pick up newly added custom extensions
def get_extensiones() -> dict:
    """Return all extensions (predefined + custom) reading fresh from disk."""
    try:
        from custom_extensions import load_all_extensions
        return load_all_extensions()
    except Exception as e:
        print(f"Warning: Could not load custom extensions: {e}")
        return EXTENSIONES_PREDEFINIDAS.copy()

# Backward-compat alias – re-evaluated each time via property-like helper
EXTENSIONES = get_extensiones()

# Folder structure category
OTROS_FOLDER = "Otros"

# File icons mapping
FILE_ICONS = {
    "Imagenes": "🖼️",
    "Documentos": "📄",
    "Videos": "🎬",
    "Musica": "🎵",
    "Comprimidos": "📦",
    "Codigo": "💻",
    "Otros": "📁",
}

# Default icon for unknown custom categories
DEFAULT_ICON = "⚙️"

# Preset folder structures
PRESET_STRUCTURES = {
    "Básico": ["Imagenes", "Documentos", "Videos", "Musica", "Comprimidos", "Codigo", "Otros"],
    "Trabajo": ["Documentos", "Presentaciones", "Hojas de cálculo", "Referencias", "Proyectos", "Otros"],
    "Multimedia": ["Imagenes", "Videos", "Musica", "Capturas", "Otros"],
    "Desarrollo": ["Codigo", "Documentos", "Recursos", "Distribuciones", "Otros"],
    "Personalizado": [],  # User-defined structure
}

PRESET_DESCRIPTIONS = {
    "Básico": "Estructura estándar para organización general de archivos.",
    "Trabajo": "Carpetas orientadas a documentos, presentaciones y proyectos.",
    "Multimedia": "Estructura para imágenes, videos, música y capturas.",
    "Desarrollo": "Espacio para código, recursos y resultados de compilación.",
    "Personalizado": "Crea tu propia estructura de carpetas según tus necesidades.",
}

# UI Configuration
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 760
THEME = "blue"
APPEARANCE_MODE = "light"
