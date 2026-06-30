# Structura 📁

**Aplicación de escritorio para organizar y gestionar la estructura de carpetas de forma visual e intuitiva.**

Desarrollada con Python y CustomTkinter. Compatible con **Windows**, **Linux** y **macOS**.

---

## ✨ Características principales

- 🌳 **Explorador visual** — Árbol de carpetas interactivo en tiempo real.
- ⚡ **Organización automática** — Clasifica los archivos de una carpeta por tipo (imágenes, documentos, vídeos, código, etc.) con un solo clic.
- 📦 **Sistema de presets** — Presets predefinidos de estructuras de carpetas (Básico, Trabajo, Multimedia, Desarrollo) y editor para crear los tuyos propios.
- 🌲 **Editor de presets avanzado** — Árbol jerárquico con soporte de **arrastrar y soltar** (drag & drop) para diseñar tus propias estructuras de carpetas.
- 🗑️ **Limpieza inteligente** — Detecta y elimina carpetas vacías para mantener el directorio ordenado.
- 🌙 **Tema oscuro/claro** — Se adapta automáticamente al tema del sistema operativo.
- 🌍 **Multiplataforma** — Funciona en Windows, Linux y macOS.

---

## 🛠️ Tecnologías usadas

| Tecnología | Uso |
|---|---|
| Python 3.10+ | Lenguaje principal |
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | Interfaz gráfica moderna |
| `tkinter / ttk` | Árbol de carpetas y drag & drop |
| `pathlib` | Gestión de rutas multiplataforma |
| PyInstaller | Generación de ejecutables |

---

## 🚀 Instalación

### Opción A — Instaladores automáticos (recomendado)

**Windows:** Haz doble clic en `instalar_windows.bat`

**Linux / macOS:**
```bash
chmod +x instalar_linux_mac.sh
./instalar_linux_mac.sh
```

El script instalará las dependencias, generará el ejecutable y creará un acceso directo automáticamente.

---

### Opción B — Ejecutar desde el código fuente

**Requisitos:** Python 3.10 o superior.

```bash
# 1. Clonar el repositorio
git clone https://github.com/CodeByOmar-Stack/Structura.git
cd Structura

# 2. Crear entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar
python main.py
```

---

## 📖 Cómo usarlo

1. **Elige una carpeta** con el botón "Elegir Carpeta".
2. **Organiza archivos** — El botón "Organizar Archivos" los clasifica automáticamente en subcarpetas por tipo.
3. **Crea una estructura** — Selecciona un preset y pulsa "Crear Estructura de Carpetas" para generarla.
4. **Personaliza tus presets** — Entra en "⚙️ Administrar Presets" para crear tus propias estructuras de carpetas con el editor visual de árbol.

---

## 📂 Estructura del proyecto

```
GestorCarpetas/
├── main.py               # Punto de entrada
├── ui.py                 # Interfaz gráfica (CustomTkinter + Treeview)
├── file_organizer.py     # Lógica de organización y gestión de carpetas
├── constants.py          # Presets, extensiones y configuración global
├── advanced_config.py    # Configuraciones adicionales
├── utils.py              # Funciones auxiliares
├── requirements.txt      # Dependencias Python
├── GestorCarpetas.spec   # Configuración de PyInstaller
├── instalar_windows.bat  # Instalador para Windows
├── instalar_linux_mac.sh # Instalador para Linux y macOS
└── assets/               # Recursos gráficos
```

---

## ⚙️ Compilar el ejecutable manualmente

```bash
pip install pyinstaller
pyinstaller GestorCarpetas.spec --noconfirm --clean
```

El ejecutable aparecerá en la carpeta `dist/`.

---

## 📄 Licencia

Este proyecto es de código abierto bajo la licencia [MIT](LICENSE). Puedes usarlo, modificarlo y distribuirlo libremente.
