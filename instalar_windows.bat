@echo off
REM ============================================================
REM  GestorCarpetas - Script de instalacion para Windows
REM  Requiere: Python 3.10+ instalado y en el PATH del sistema.
REM ============================================================

echo ============================================
echo  Instalador de GestorCarpetas para Windows
echo ============================================
echo.

REM Comprobar si Python esta instalado
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERROR] Python no encontrado. Por favor instala Python 3.10 o superior
    echo         desde https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Python encontrado. Creando entorno virtual...
python -m venv venv
IF ERRORLEVEL 1 (
    echo [ERROR] No se pudo crear el entorno virtual.
    pause
    exit /b 1
)

echo [2/4] Activando entorno virtual e instalando dependencias...
call venv\Scripts\activate.bat
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
IF ERRORLEVEL 1 (
    echo [ERROR] No se pudieron instalar las dependencias.
    pause
    exit /b 1
)

echo [3/4] Generando ejecutable con PyInstaller...
pyinstaller GestorCarpetas.spec --noconfirm --clean
IF ERRORLEVEL 1 (
    echo [ERROR] Fallo al generar el ejecutable.
    pause
    exit /b 1
)

echo [4/4] Creando acceso directo en el Escritorio...
set SCRIPT_DIR=%~dp0
set EXE_PATH=%SCRIPT_DIR%dist\GestorCarpetas.exe
set SHORTCUT_PATH=%USERPROFILE%\Desktop\GestorCarpetas.lnk

powershell -NoProfile -Command ^
  "$ws = New-Object -ComObject WScript.Shell; ^
   $s = $ws.CreateShortcut('%SHORTCUT_PATH%'); ^
   $s.TargetPath = '%EXE_PATH%'; ^
   $s.WorkingDirectory = '%SCRIPT_DIR%dist'; ^
   $s.Description = 'GestorCarpetas - Organizador de Archivos'; ^
   $s.Save()"

echo.
echo ============================================
echo  Instalacion completada con exito!
echo  Ejecutable: dist\GestorCarpetas.exe
echo  Acceso directo creado en el Escritorio.
echo ============================================
pause
