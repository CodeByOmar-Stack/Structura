"""
ARQUITECTURA DEL PROYECTO - GestorCarpetas

Este documento describe la estructura y organización del proyecto.
"""

# ============================================================================
# DIAGRAMA DE FLUJO - ORGANIZACIÓN DE ARCHIVOS
# ============================================================================

"""
┌─────────────────────────────────────────────────────────────────────────┐
│                    GESTOR CARPETAS - FLUJO PRINCIPAL                    │
└─────────────────────────────────────────────────────────────────────────┘

1. INICIO
   ↓
2. Usuario selecciona carpeta
   ↓
3. UI actualiza vista (Treeview)
   ↓
4. Usuario hace clic en "Organizar"
   ↓
5. Confirmación del usuario
   ↓
6. FileOrganizer.organize_files()
   ├─ Crea carpetas por categoría
   ├─ Itera sobre archivos
   ├─ Clasifica por extensión
   └─ Mueve a carpeta correspondiente
   ↓
7. UI actualiza log con resultados
   ↓
8. UI actualiza vista (Treeview)
"""

# ============================================================================
# ESTRUCTURA DE MÓDULOS
# ============================================================================

"""
GestorCarpetas/
│
├── main.py                  ← Punto de entrada
│   └── Inicializa GestorCarpetasUI
│
├── constants.py             ← Configuración centralizada
│   ├── EXTENSIONES          (categorías de archivos)
│   ├── FILE_ICONS           (emojis por categoría)
│   ├── WINDOW_WIDTH/HEIGHT  (tamaño ventana)
│   └── THEME/APPEARANCE     (tema UI)
│
├── advanced_config.py       ← Configuración avanzada
│   ├── COLOR_SCHEMES        (temas de color)
│   ├── FILE_EMOJIS          (emojis extendidos)
│   ├── IGNORED_FOLDERS      (carpetas a ignorar)
│   └── AUTO_BACKUP          (configuración backup)
│
├── file_organizer.py        ← Lógica de negocio
│   └── FileOrganizer class
│       ├── set_folder()
│       ├── create_category_folders()
│       ├── organize_files()
│       └── get_folder_structure()
│
├── utils.py                 ← Funciones auxiliares
│   ├── get_file_icon()
│   ├── get_human_readable_size()
│   ├── get_folder_statistics()
│   ├── create_backup()
│   ├── restore_from_backup()
│   └── get_duplicate_files()
│
├── ui.py                    ← Interfaz gráfica
│   ├── GestorCarpetasUI     (ventana principal)
│   ├── FolderTreeView       (explorador de carpetas)
│   └── StatusPanel          (panel de estado/log)
│
├── requirements.txt         ← Dependencias
├── README.md               ← Documentación
└── assets/                 ← Recursos (iconos, etc)
"""

# ============================================================================
# COMPONENTES PRINCIPALES
# ============================================================================

"""
1. FILE_ORGANIZER.PY - FileOrganizer
   ├─ Responsabilidad: Lógica de organización
   ├─ Independencia: No depende de UI
   ├─ Reutilizable: Puede usarse en CLI o scripts
   └─ Métodos:
       ├─ set_folder(path)              → Establece carpeta objetivo
       ├─ create_category_folders()     → Crea carpetas de categorías
       ├─ organize_files()              → Organiza archivos
       └─ get_folder_structure()        → Obtiene estructura

2. UI.PY - GestorCarpetasUI
   ├─ Responsabilidad: Interfaz gráfica
   ├─ Componentes:
   │  ├─ FolderTreeView       (visualización jerárquica)
   │  └─ StatusPanel          (log de operaciones)
   └─ Métodos:
       ├─ select_folder()             → Diálogo de selección
       ├─ organize_files()            → Inicia organización
       ├─ refresh_view()              → Actualiza vista
       └─ add_log_message()           → Añade al log

3. CONSTANTS.PY - Configuración centralizada
   ├─ EXTENSIONES              (tipos de archivos)
   ├─ FILE_ICONS              (iconos visuales)
   └─ UI Config               (dimensiones, temas)

4. UTILS.PY - Funciones auxiliares
   ├─ Operaciones de archivo
   ├─ Cálculo de estadísticas
   ├─ Gestión de backup
   └─ Búsqueda de duplicados
"""

# ============================================================================
# FLUJO DE DATOS
# ============================================================================

"""
┌──────────────────────────────────────────────────────────────────────┐
│                         FLUJO DE DATOS                               │
└──────────────────────────────────────────────────────────────────────┘

USER INTERACTION (UI)
    ↓
    ├─→ Select Folder Dialog
    │   ├─ User selects path
    │   ├─ GestorCarpetasUI.select_folder()
    │   └─ FileOrganizer.set_folder(path) ✓
    │
    ├─→ Display Folder Structure
    │   ├─ FileOrganizer.get_folder_structure()
    │   ├─ FolderTreeView.display_tree()
    │   └─ Treeview rendered
    │
    └─→ Organize Files
        ├─ Confirmation Dialog (User)
        ├─ FileOrganizer.organize_files()
        │  ├─ Create category folders
        │  ├─ Classify each file
        │  ├─ Move files
        │  └─ Generate statistics
        ├─ Callback messages → StatusPanel
        ├─ UI.refresh_view()
        └─ Display results
"""

# ============================================================================
# EXTENSIBILIDAD
# ============================================================================

"""
Cómo agregar nuevas características:

1. NUEVA CATEGORÍA DE ARCHIVOS
   ├─ Editar: constants.py → EXTENSIONES
   └─ Ejemplo: "Ejecutables": [".exe", ".bat", ".sh"]

2. NUEVA FUNCIONALIDAD DE ORGANIZACIÓN
   ├─ Agregar método a: file_organizer.py → FileOrganizer
   └─ Exponer en UI: ui.py → GestorCarpetasUI

3. NUEVO TIPO DE VISTA
   ├─ Crear clase en: ui.py
   ├─ Heredar de: ctk.CTkFrame
   └─ Integrar en: GestorCarpetasUI._create_widgets()

4. NUEVAS UTILIDADES
   ├─ Agregar función a: utils.py
   └─ Importar donde sea necesario: from utils import ...

5. NUEVO TEMA
   ├─ Editar: advanced_config.py → COLOR_SCHEMES
   └─ Usar en: ui.py → GestorCarpetasUI
"""

# ============================================================================
# PATRONES DE DISEÑO UTILIZADOS
# ============================================================================

"""
1. SEPARACIÓN DE RESPONSABILIDADES
   ├─ UI (visualización) ← → FileOrganizer (lógica)
   ├─ Constants (configuración)
   └─ Utils (utilidades)

2. CALLBACK PATTERN
   ├─ FileOrganizer acepta callback
   └─ Reporta estado a UI en tiempo real

3. SINGLETON PATTERN (implícito)
   ├─ Una instancia de GestorCarpetasUI
   └─ Una instancia de FileOrganizer

4. MVC (Model-View-Controller)
   ├─ Model: FileOrganizer + Constants
   ├─ View: UI (GestorCarpetasUI, FolderTreeView)
   └─ Controller: GestorCarpetasUI methods
"""

# ============================================================================
# TESTING Y MANTENIMIENTO
# ============================================================================

"""
Para agregar tests (recomendado):

test_file_organizer.py
├─ test_set_folder()
├─ test_organize_files()
├─ test_category_creation()
└─ test_folder_structure()

test_utils.py
├─ test_get_file_icon()
├─ test_get_human_readable_size()
└─ test_get_folder_statistics()

Ejecución: python -m pytest
"""

print("ARQUITECTURA DEL PROYECTO - GestorCarpetas")
print("Ver este archivo para documentación completa")
