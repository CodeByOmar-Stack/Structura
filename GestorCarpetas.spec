# -*- mode: python ; coding: utf-8 -*-
# GestorCarpetas.spec
# Archivo de configuración de PyInstaller para construir el ejecutable.
# Uso: pyinstaller GestorCarpetas.spec

import sys
from pathlib import Path

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('constants.py', '.'),
        ('custom_extensions.py', '.'),
        ('file_organizer.py', '.'),
        ('ui.py', '.'),
        ('utils.py', '.'),
        ('advanced_config.py', '.'),
    ],
    hiddenimports=[
        'customtkinter',
        'darkdetect',
        'PIL',
        'PIL.Image',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GestorCarpetas',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    # En Windows se muestra sin consola (windowed). En Linux/Mac también.
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    # Icono: descomenta la línea siguiente si tienes un archivo .ico (Windows) o .icns (Mac)
    # icon='assets/icon.ico',
)

# Solo en macOS: empaqueta como .app
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='GestorCarpetas.app',
        # icon='assets/icon.icns',
        bundle_identifier='com.gestorcarpetas.app',
        info_plist={
            'NSHighResolutionCapable': True,
            'CFBundleShortVersionString': '1.0.0',
        },
    )
