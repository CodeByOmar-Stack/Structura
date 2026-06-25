#!/bin/bash
# ============================================================
#  GestorCarpetas - Script de instalacion para Linux y macOS
#  Requiere: Python 3.10+ instalado en el sistema.
# ============================================================

set -e  # Salir si cualquier comando falla

echo "============================================"
echo " Instalador de GestorCarpetas para Linux/Mac"
echo "============================================"
echo ""

# ---- Detectar el sistema operativo ----
OS="$(uname -s)"
case "$OS" in
    Linux*)   PLATFORM="Linux" ;;
    Darwin*)  PLATFORM="macOS" ;;
    *)        echo "[ERROR] Sistema operativo no soportado: $OS"; exit 1 ;;
esac
echo "Sistema detectado: $PLATFORM"

# ---- Comprobar Python ----
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 no encontrado."
    if [ "$PLATFORM" = "Linux" ]; then
        echo "  Instálalo con: sudo apt install python3 python3-venv (Debian/Ubuntu)"
        echo "                 sudo dnf install python3 (Fedora)"
    else
        echo "  Instálalo desde: https://www.python.org/downloads/"
    fi
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "[1/4] Python $PYTHON_VERSION encontrado. Creando entorno virtual..."

# ---- Dependencias de sistema para tkinter en Linux ----
if [ "$PLATFORM" = "Linux" ]; then
    if ! python3 -c "import tkinter" 2>/dev/null; then
        echo "      Instalando tkinter del sistema (requiere sudo)..."
        if command -v apt &>/dev/null; then
            sudo apt-get install -y python3-tk
        elif command -v dnf &>/dev/null; then
            sudo dnf install -y python3-tkinter
        elif command -v pacman &>/dev/null; then
            sudo pacman -S --noconfirm tk
        fi
    fi
fi

# ---- Crear entorno virtual ----
python3 -m venv venv
echo "[2/4] Entorno virtual creado. Instalando dependencias..."

source venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo "[3/4] Generando ejecutable con PyInstaller..."
pyinstaller GestorCarpetas.spec --noconfirm --clean

# ---- Crear lanzador ----
echo "[4/4] Creando lanzador..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "$PLATFORM" = "macOS" ]; then
    # En macOS: instalar el .app en /Applications
    if [ -d "dist/GestorCarpetas.app" ]; then
        echo "      Copiando GestorCarpetas.app a /Applications (puede pedir contraseña)..."
        sudo cp -r "dist/GestorCarpetas.app" "/Applications/"
        echo "      Aplicación instalada en /Applications/GestorCarpetas.app"
    fi
else
    # En Linux: crear un .desktop para el menú de aplicaciones y el escritorio
    EXEC_PATH="$SCRIPT_DIR/dist/GestorCarpetas"
    DESKTOP_FILE="$HOME/.local/share/applications/gestorcarpetas.desktop"
    DESKTOP_SHORTCUT="$HOME/Desktop/GestorCarpetas.desktop"

    mkdir -p "$HOME/.local/share/applications"

    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=GestorCarpetas
Comment=Organizador de Archivos
Exec=$EXEC_PATH
Terminal=false
Categories=Utility;FileManager;
EOF

    # Copiar al escritorio si existe
    if [ -d "$HOME/Desktop" ]; then
        cp "$DESKTOP_FILE" "$DESKTOP_SHORTCUT"
        chmod +x "$DESKTOP_SHORTCUT"
        echo "      Acceso directo creado en el Escritorio."
    elif [ -d "$HOME/Escritorio" ]; then
        cp "$DESKTOP_FILE" "$HOME/Escritorio/GestorCarpetas.desktop"
        chmod +x "$HOME/Escritorio/GestorCarpetas.desktop"
        echo "      Acceso directo creado en el Escritorio."
    fi

    chmod +x "$EXEC_PATH"
    echo "      Lanzador añadido al menú de aplicaciones."
fi

echo ""
echo "============================================"
echo " Instalacion completada con exito!"
if [ "$PLATFORM" = "macOS" ]; then
    echo " Abre 'GestorCarpetas' desde el Launchpad o /Applications."
else
    echo " Ejecutable: dist/GestorCarpetas"
    echo " Busca 'GestorCarpetas' en tu menú de aplicaciones."
fi
echo "============================================"
