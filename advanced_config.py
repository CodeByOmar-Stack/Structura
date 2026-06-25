"""Configuration file for GestorCarpetas - Advanced Settings"""

# Color scheme presets
COLOR_SCHEMES = {
    "blue": {
        "primary": "#0084FF",
        "secondary": "#E3F2FD",
        "text": "#FFFFFF",
        "background": "#1E1E1E",
    },
    "green": {
        "primary": "#4CAF50",
        "secondary": "#E8F5E9",
        "text": "#FFFFFF",
        "background": "#1B1B1B",
    },
    "purple": {
        "primary": "#9C27B0",
        "secondary": "#F3E5F5",
        "text": "#FFFFFF",
        "background": "#1A1A1A",
    },
}

# File type to emoji mapping (extended)
FILE_EMOJIS = {
    # Images
    ".jpg": "🖼️", ".jpeg": "🖼️", ".png": "🖼️", ".gif": "🖼️", ".bmp": "🖼️",
    ".svg": "🖼️", ".webp": "🖼️", ".tiff": "🖼️",
    
    # Documents
    ".pdf": "📕", ".doc": "📘", ".docx": "📘", ".txt": "📄",
    ".xls": "📗", ".xlsx": "📗", ".ppt": "📙", ".pptx": "📙",
    ".odt": "📄",
    
    # Videos
    ".mp4": "🎬", ".avi": "🎬", ".mov": "🎬", ".mkv": "🎬",
    ".flv": "🎬", ".wmv": "🎬", ".webm": "🎬", ".m4v": "🎬",
    
    # Audio
    ".mp3": "🎵", ".wav": "🎵", ".aac": "🎵", ".flac": "🎵",
    ".ogg": "🎵", ".wma": "🎵", ".m4a": "🎵",
    
    # Archives
    ".zip": "📦", ".rar": "📦", ".7z": "📦", ".tar": "📦",
    ".gz": "📦", ".bz2": "📦",
    
    # Code
    ".py": "🐍", ".js": "⚙️", ".html": "🌐", ".css": "🎨",
    ".java": "☕", ".cpp": "⚙️", ".c": "⚙️", ".go": "🐹", ".rs": "🦀",
    ".json": "📋", ".xml": "📋", ".yaml": "📋", ".sql": "🗄️",
    
    # Default
    "default": "📄",
}

# Ignored folders (will not be scanned)
IGNORED_FOLDERS = {
    ".git", ".venv", "__pycache__", "node_modules",
    ".cache", ".config", ".local", "AppData",
}

# Maximum log lines to display
MAX_LOG_LINES = 100

# Auto-backup before organizing (True/False)
AUTO_BACKUP = False

# Backup folder name (if auto-backup is enabled)
BACKUP_FOLDER = ".backup_organizer"
