"""Configuration and constants for GestorCarpetas."""

# File extensions by category
EXTENSIONES = {
    "Imagenes": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg"],
    "Documentos": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".odt"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm", ".m4v"],
    "Musica": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".m4a"],
    "Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Codigo": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".go", ".rs"],
}

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

# Preset folder structures
PRESET_STRUCTURES = {
    "Básico": ["Imagenes", "Documentos", "Videos", "Musica", "Comprimidos", "Codigo", "Otros"],
    "Trabajo": ["Documentos", "Presentaciones", "Hojas de cálculo", "Referencias", "Proyectos", "Otros"],
    "Multimedia": ["Imagenes", "Videos", "Musica", "Capturas", "Otros"],
    "Desarrollo": ["Codigo", "Documentos", "Recursos", "Distribuciones", "Otros"],
}

PRESET_DESCRIPTIONS = {
    "Básico": "Estructura estándar para organización general de archivos.",
    "Trabajo": "Carpetas orientadas a documentos, presentaciones y proyectos.",
    "Multimedia": "Estructura para imágenes, videos, música y capturas.",
    "Desarrollo": "Espacio para código, recursos y resultados de compilación.",
}

# UI Configuration
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
THEME = "blue"
APPEARANCE_MODE = "system"
