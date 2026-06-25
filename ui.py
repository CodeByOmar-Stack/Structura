"""UI components for GestorCarpetas."""

import customtkinter as ctk
import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    THEME,
    APPEARANCE_MODE,
    FILE_ICONS,
    EXTENSIONES,
    PRESET_STRUCTURES,
    PRESET_DESCRIPTIONS,
)
from file_organizer import FileOrganizer


class FolderTreeView(ctk.CTkFrame):
    """Custom tree view for displaying folder structure."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Create treeview with scrollbar
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame)
        scrollbar.pack(side="right", fill="y")

        # Treeview
        self.tree = ttk.Treeview(
            self.tree_frame,
            yscrollcommand=scrollbar.set,
            height=20,
        )
        scrollbar.configure(command=self.tree.yview)
        self.tree.pack(side="left", fill="both", expand=True)

        # Configure style
        style = ttk.Style()
        style.theme_use("clam")

        self.tree.heading("#0", text="Estructura de Carpetas")
        self.tree.column("#0", width=400)

    def display_tree(self, folder_path: str):
        """Display the folder structure in the tree."""
        self.tree.delete(*self.tree.get_children())
        
        path = Path(folder_path)
        if not path.exists():
            return

        root_id = self.tree.insert("", "end", text=f"📁 {path.name}", open=True)
        self._build_tree(path, root_id)

    def _build_tree(self, path: Path, parent_id: str):
        """Recursively build tree items."""
        try:
            items = sorted(
                path.iterdir(),
                key=lambda x: (not x.is_dir(), x.name.lower())
            )

            for item in items:
                if item.is_dir():
                    # Skip hidden folders
                    if item.name.startswith("."):
                        continue
                    
                    # Get file count in folder
                    file_count = len([f for f in item.iterdir() if f.is_file()])
                    display_name = f"📁 {item.name}"
                    if file_count > 0:
                        display_name += f" ({file_count})"
                    
                    node_id = self.tree.insert(parent_id, "end", text=display_name)
                    self._build_tree(item, node_id)
                else:
                    icon = self._get_file_icon(item.suffix)
                    size_kb = item.stat().st_size / 1024
                    display_name = f"{icon} {item.name} ({size_kb:.1f}KB)"
                    self.tree.insert(parent_id, "end", text=display_name)
        except PermissionError:
            pass

    @staticmethod
    def _get_file_icon(extension: str) -> str:
        """Get icon for file based on extension."""
        ext = extension.lower()
        for category, extensions in EXTENSIONES.items():
            if ext in extensions:
                return FILE_ICONS.get(category, "📄")
        return FILE_ICONS.get("Otros", "📄")





class PresetEditor(ctk.CTkToplevel):
    """Popup window to create and preview folder structures."""

    def __init__(self, parent, presets, descriptions, on_apply, on_preset_saved=None, new_preset=False, base_structure=None):
        super().__init__(parent)
        self.title("Editor de Presets")
        self.geometry("550x650")
        self.resizable(True, True)
        self.attributes("-topmost", True)
        self.transient(parent)
        self.presets = presets
        self.descriptions = descriptions
        self.on_apply = on_apply
        self.on_preset_saved = on_preset_saved
        self.new_preset = new_preset
        self.folder_list = list(base_structure) if base_structure else []

        self._create_widgets()
        if presets and not self.new_preset:
            self.select_preset(list(presets.keys())[0])
        else:
            self.start_new_preset()

    def _create_widgets(self):
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            top_frame,
            text="Seleccionar preset",
            font=("Arial", 12, "bold"),
        ).pack(anchor="w", pady=(0, 5))

        option_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        option_frame.pack(fill="x")

        self.preset_option = ctk.CTkOptionMenu(
            option_frame,
            values=list(self.presets.keys()),
            command=self.select_preset,
        )
        self.preset_option.pack(side="left", fill="x", expand=True, padx=(0, 5))

        add_preset_btn = ctk.CTkButton(
            option_frame,
            text="➕",
            width=35,
            command=self.start_new_preset,
            fg_color="#1565C0",
            hover_color="#1E88E5",
        )
        add_preset_btn.pack(side="right")

        self.description_label = ctk.CTkLabel(
            top_frame,
            text="",
            font=("Arial", 10),
            wraplength=460,
            justify="left",
            text_color="gray",
        )
        self.description_label.pack(anchor="w", pady=(8, 0))

        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.pack(side="bottom", fill="x", padx=15, pady=(0, 15))

        save_frame = ctk.CTkFrame(self)
        save_frame.pack(side="bottom", fill="x", padx=15, pady=(0, 5))

        editor_frame = ctk.CTkFrame(self)
        editor_frame.pack(fill="both", expand=True, padx=15, pady=10)

        preview_label = ctk.CTkLabel(
            editor_frame,
            text="Vista previa de la estructura",
            font=("Arial", 11, "bold"),
        )
        preview_label.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))

        list_frame = ctk.CTkFrame(editor_frame)
        list_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(0, 10))

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
            background="#2B2B2B",
            foreground="#FFFFFF",
            fieldbackground="#2B2B2B",
            borderwidth=0
        )
        style.map('Treeview', background=[('selected', '#1F538D')])

        self.folder_tree = ttk.Treeview(list_frame, selectmode="browse", show="tree")
        self.folder_tree.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=(0, 0))

        list_scroll = ttk.Scrollbar(list_frame, command=self.folder_tree.yview)
        list_scroll.pack(side="right", fill="y")
        self.folder_tree.configure(yscrollcommand=list_scroll.set)

        self.folder_tree.bind("<ButtonPress-1>", self._on_drag_start)
        self.folder_tree.bind("<B1-Motion>", self._on_drag_motion)
        self.folder_tree.bind("<ButtonRelease-1>", self._on_drop)

        self.new_folder_entry = ctk.CTkEntry(
            editor_frame,
            placeholder_text="Por ejemplo: Proyectos/APP",
        )
        self.new_folder_entry.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.new_folder_entry.bind("<Return>", lambda event: self.add_folder())

        add_button = ctk.CTkButton(
            editor_frame,
            text="Agregar carpeta",
            command=self.add_folder,
            width=150,
        )
        add_button.grid(row=2, column=2, padx=(10, 0), pady=(0, 10), sticky="e")

        remove_button = ctk.CTkButton(
            editor_frame,
            text="Eliminar seleccionada",
            command=self.remove_folder,
            fg_color="#C62828",
            hover_color="#D32F2F",
            width=150,
        )
        remove_button.grid(row=3, column=0, pady=(0, 5), sticky="w")

        clear_button = ctk.CTkButton(
            editor_frame,
            text="Limpiar lista",
            command=self.clear_folders,
            width=150,
        )
        clear_button.grid(row=3, column=1, pady=(0, 5), sticky="e")

        editor_frame.grid_columnconfigure(0, weight=1)
        editor_frame.grid_columnconfigure(1, weight=0)
        editor_frame.grid_columnconfigure(2, weight=0)
        editor_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            save_frame,
            text="Guardar preset",
            font=("Arial", 11, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        self.new_preset_name = ctk.CTkEntry(
            save_frame,
            placeholder_text="Nombre del preset",
        )
        self.new_preset_name.grid(row=1, column=0, sticky="ew", pady=(0, 5))

        self.new_preset_description = ctk.CTkEntry(
            save_frame,
            placeholder_text="Descripción breve (opcional)",
        )
        self.new_preset_description.grid(row=2, column=0, sticky="ew", pady=(0, 8))

        save_button = ctk.CTkButton(
            save_frame,
            text="Guardar preset",
            command=self.save_preset,
            width=150,
        )
        save_button.grid(row=1, column=1, rowspan=2, padx=(10, 0), sticky="nsew")



        save_frame.grid_columnconfigure(0, weight=1)
        save_frame.grid_columnconfigure(1, weight=0)

        apply_button = ctk.CTkButton(
            bottom_frame,
            text="Aplicar estructura",
            command=self.apply_structure,
            height=40,
        )
        apply_button.pack(side="left", fill="x", expand=True, padx=(0, 10))

        close_button = ctk.CTkButton(
            bottom_frame,
            text="Cerrar",
            command=self.destroy,
            fg_color="#757575",
            hover_color="#9E9E9E",
            height=40,
            width=120,
        )
        close_button.pack(side="right")

    def select_preset(self, preset_name: str):
        self.new_preset = False
        self.folder_list = list(self.presets.get(preset_name, []))
        if hasattr(self, 'preset_option'):
            self.preset_option.set(preset_name)
        if hasattr(self, 'description_label'):
            self.description_label.configure(text=self.descriptions.get(preset_name, ""))
            
        if hasattr(self, 'new_preset_name'):
            self.new_preset_name.delete(0, "end")
            self.new_preset_name.insert(0, preset_name)
        if hasattr(self, 'new_preset_description'):
            self.new_preset_description.delete(0, "end")
            self.new_preset_description.insert(0, self.descriptions.get(preset_name, ""))
            
        self.refresh_preview()

    def _get_all_paths(self, tree, item="", current_path=""):
        paths = []
        for child in tree.get_children(item):
            text = tree.item(child, "text")
            path = f"{current_path}/{text}" if current_path else text
            paths.append(path)
            paths.extend(self._get_all_paths(tree, child, path))
        return paths

    def refresh_preview(self):
        if hasattr(self, 'folder_tree'):
            self.folder_tree.delete(*self.folder_tree.get_children())
            for path in sorted(self.folder_list):
                parts = path.split("/")
                parent = ""
                for i, part in enumerate(parts):
                    node_id = "/".join(parts[:i+1])
                    if not self.folder_tree.exists(node_id):
                        self.folder_tree.insert(parent, "end", iid=node_id, text=part, open=True)
                    parent = node_id

    def add_folder(self):
        folder_name = self.new_folder_entry.get().strip()
        if not folder_name:
            return
            
        folder_name = folder_name.strip("/")
        
        selected = self.folder_tree.selection()
        if selected and "/" not in folder_name:
            parent_path = selected[0]
            full_path = f"{parent_path}/{folder_name}"
        else:
            full_path = folder_name
            
        if full_path not in self.folder_list:
            self.folder_list.append(full_path)
            self.refresh_preview()
            self.new_folder_entry.delete(0, "end")

    def remove_folder(self):
        selected = self.folder_tree.selection()
        if not selected:
            return
        for item in selected:
            if self.folder_tree.exists(item):
                self.folder_tree.delete(item)
        self.folder_list = self._get_all_paths(self.folder_tree)
        self.refresh_preview()

    def clear_folders(self):
        self.folder_list = []
        self.refresh_preview()

    def _on_drag_start(self, event):
        item = self.folder_tree.identify_row(event.y)
        if item:
            self._dragged_item = item

    def _on_drag_motion(self, event):
        pass

    def _on_drop(self, event):
        if not hasattr(self, '_dragged_item') or not self._dragged_item:
            return
        target_item = self.folder_tree.identify_row(event.y)
        
        if target_item == self._dragged_item:
            self._dragged_item = None
            return
            
        curr = target_item
        while curr:
            if curr == self._dragged_item:
                self._dragged_item = None
                return
            curr = self.folder_tree.parent(curr)

        if target_item:
            self.folder_tree.move(self._dragged_item, target_item, "end")
            self.folder_tree.item(target_item, open=True)
        else:
            self.folder_tree.move(self._dragged_item, "", "end")
            
        self.folder_list = self._get_all_paths(self.folder_tree)
        self.refresh_preview()
        self._dragged_item = None

    def start_new_preset(self):
        self.folder_list = []
        if hasattr(self, 'new_preset_name'):
            self.new_preset_name.delete(0, "end")
            self.focus()
            self.new_preset_name.focus()
        if hasattr(self, 'new_preset_description'):
            self.new_preset_description.delete(0, "end")
        self.new_preset = True
        if hasattr(self, 'preset_option') and self.preset_option:
            self.preset_option.set("Nuevo preset")
        self.refresh_preview()

    def save_preset(self):
        preset_name = self.new_preset_name.get().strip()
        if not preset_name:
            messagebox.showwarning("Advertencia", "Introduce un nombre para el preset.")
            return
            
        current_selection = self.preset_option.get() if hasattr(self, 'preset_option') else ""
        
        if preset_name in self.presets:
            if self.new_preset or preset_name != current_selection:
                confirm = messagebox.askyesno("Sobrescribir", f"El preset '{preset_name}' ya existe. ¿Deseas sobrescribirlo?")
                if not confirm:
                    return

        self.presets[preset_name] = list(self.folder_list)
        self.descriptions[preset_name] = self.new_preset_description.get().strip() or "Preset personalizado"
        if hasattr(self, 'preset_option'):
            self.preset_option.configure(values=list(self.presets.keys()))
            self.preset_option.set(preset_name)
        if hasattr(self, 'description_label'):
            self.description_label.configure(text=self.descriptions.get(preset_name, ""))
            
        self.new_preset = False
        if self.on_preset_saved:
            self.on_preset_saved(preset_name)
        messagebox.showinfo("Éxito", f"Preset '{preset_name}' guardado.")

    def apply_structure(self):
        if not self.folder_list:
            messagebox.showwarning(
                "Advertencia",
                "La estructura está vacía. Agrega carpetas o selecciona un preset.",
            )
            return

        if self.on_apply(self.folder_list):
            self.refresh_preview()
            self.destroy()


class GestorCarpetasUI:
    """Main UI class for GestorCarpetas."""

    def __init__(self):
        # Setup appearance
        ctk.set_appearance_mode(APPEARANCE_MODE)
        ctk.set_default_color_theme(THEME)

        # Create main window
        self.app = ctk.CTk()
        self.app.title("🗂️ GestorCarpetas - Organizador de Archivos")
        self.app.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.app.resizable(True, True)

        # File organizer
        self.organizer = FileOrganizer(callback=self.add_log_message)
        self.selected_folder = None

        # Create UI
        self._create_widgets()

    def _create_widgets(self):
        """Create all UI widgets."""
        # Main container
        main_container = ctk.CTkFrame(self.app)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Main content area
        content_frame = ctk.CTkFrame(main_container)
        content_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Left panel - Folder tree
        left_panel = ctk.CTkFrame(content_frame)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))

        title_tree = ctk.CTkLabel(
            left_panel,
            text="🌳 Explorador de Carpetas",
            font=("Arial", 14, "bold"),
        )
        title_tree.pack(anchor="w", padx=10, pady=(10, 5))

        self.folder_tree = FolderTreeView(left_panel)
        self.folder_tree.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        # Right panel - Status and options
        right_panel = ctk.CTkFrame(content_frame)
        right_panel.pack(side="right", fill="both", expand=False, padx=(5, 0))

        # 1. Folder Selection
        folder_frame = ctk.CTkFrame(right_panel)
        folder_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        title_folder = ctk.CTkLabel(
            folder_frame,
            text="1. Seleccionar Carpeta",
            font=("Arial", 12, "bold"),
        )
        title_folder.pack(anchor="w", pady=(0, 5))

        button_select = ctk.CTkButton(
            folder_frame,
            text="📁 Elegir Carpeta",
            command=self.select_folder,
            height=35,
        )
        button_select.pack(fill="x", pady=(0, 5))

        self.folder_label = ctk.CTkLabel(
            folder_frame,
            text="Ninguna seleccionada",
            text_color="gray",
            wraplength=260
        )
        self.folder_label.pack(fill="x", pady=(0, 5))

        # 2. Main Action
        action_frame = ctk.CTkFrame(right_panel)
        action_frame.pack(fill="x", padx=10, pady=5)

        title_action = ctk.CTkLabel(
            action_frame,
            text="2. Acción Principal",
            font=("Arial", 12, "bold"),
        )
        title_action.pack(anchor="w", pady=(0, 5))

        button_organize = ctk.CTkButton(
            action_frame,
            text="🚀 Organizar Archivos",
            command=self.organize_files,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="#2E7D32",
            hover_color="#388E3C",
        )
        button_organize.pack(fill="x", pady=(0, 5))

        button_open_folder = ctk.CTkButton(
            action_frame,
            text="📂 Abrir en Explorador",
            command=self.open_folder,
            height=35,
            fg_color="#1976D2",
            hover_color="#1E88E5",
        )
        button_open_folder.pack(fill="x", pady=(0, 5))

        # 3. Structure
        struct_frame = ctk.CTkFrame(right_panel)
        struct_frame.pack(fill="x", padx=10, pady=5)

        title_struct = ctk.CTkLabel(
            struct_frame,
            text="3. Opciones de Carpetas",
            font=("Arial", 12, "bold"),
        )
        title_struct.pack(anchor="w", pady=(0, 5))

        self.preset_option = ctk.CTkOptionMenu(
            struct_frame,
            values=list(PRESET_STRUCTURES.keys()),
            command=self.on_preset_selected,
        )
        self.preset_option.set(list(PRESET_STRUCTURES.keys())[0])
        self.preset_option.pack(fill="x", pady=(0, 5))

        self.preset_description = ctk.CTkLabel(
            struct_frame,
            text=PRESET_DESCRIPTIONS.get(list(PRESET_STRUCTURES.keys())[0], ""),
            font=("Arial", 10),
            wraplength=260,
            justify="left",
            text_color="gray",
        )
        self.preset_description.pack(anchor="w", pady=(0, 5))

        button_create_structure = ctk.CTkButton(
            struct_frame,
            text="✅ Crear Estrcutra de Carpetas",
            command=self.create_structure,
            fg_color="#FBC02D",
            hover_color="#F9A825",
            text_color="black",
            height=35,
        )
        button_create_structure.pack(fill="x", pady=(0, 5))

        button_manage_presets = ctk.CTkButton(
            struct_frame,
            text="⚙️ Administrar Presets",
            command=self.open_preset_editor,
            fg_color="#2E7D32",
            hover_color="#388E3C",
            height=35,
        )
        button_manage_presets.pack(fill="x", pady=(0, 5))

        button_delete_folders = ctk.CTkButton(
            struct_frame,
            text="🗑️ Eliminar Carpetas Vacías",
            command=self.delete_structure,
            fg_color="#C62828",
            hover_color="#D32F2F",
            height=35,
        )
        button_delete_folders.pack(fill="x", pady=(0, 5))

        # Bottom bar - Action buttons and status
        bottom_bar = ctk.CTkFrame(main_container)
        bottom_bar.pack(side="bottom", fill="x")

        button_refresh = ctk.CTkButton(
            bottom_bar,
            text="🔄 Actualizar Vista",
            command=self.refresh_view,
            height=35,
            width=150,
        )
        button_refresh.pack(side="left", padx=5, pady=5)
        
        self.status_label = ctk.CTkLabel(
            bottom_bar,
            text="Listo",
            text_color="gray",
            font=("Arial", 11)
        )
        self.status_label.pack(side="right", padx=15, pady=5)

    def select_folder(self):
        """Open folder selection dialog."""
        folder = filedialog.askdirectory(title="Seleccionar carpeta a organizar")
        if folder:
            self.selected_folder = folder
            self.folder_label.configure(text=f"✅ {Path(folder).name}")
            self.organizer.set_folder(folder)
            self.refresh_view()

    def on_preset_selected(self, preset_name: str):
        """Update preset description when selection changes."""
        self.preset_description.configure(
            text=PRESET_DESCRIPTIONS.get(preset_name, "")
        )

    def open_preset_editor(self):
        """Open the preset editor window."""
        PresetEditor(
            self.app,
            PRESET_STRUCTURES,
            PRESET_DESCRIPTIONS,
            self.apply_custom_structure,
            on_preset_saved=self.on_preset_saved,
        )



    def on_preset_saved(self, preset_name: str):
        self.preset_option.configure(values=list(PRESET_STRUCTURES.keys()))
        self.preset_option.set(preset_name)
        self.preset_description.configure(
            text=PRESET_DESCRIPTIONS.get(preset_name, "")
        )

    def apply_custom_structure(self, folder_list: list[str]) -> bool:
        if not self.selected_folder:
            folder = filedialog.askdirectory(title="Seleccionar carpeta donde crear las carpetas")
            if folder:
                self.selected_folder = folder
                self.folder_label.configure(text=f"✅ {Path(folder).name}")
                self.organizer.set_folder(folder)
            else:
                return False

        result = self.organizer.create_folder_structure(folders=folder_list)
        if result:
            self.refresh_view()
        return result

    def create_structure(self):
        """Create the selected preset folder structure."""
        if not self.selected_folder:
            messagebox.showwarning(
                "Advertencia",
                "Por favor, selecciona una carpeta primero.",
            )
            return

        preset_name = self.preset_option.get()
        if self.organizer.create_folder_structure(preset_name):
            self.refresh_view()

    def delete_structure(self):
        """Delete the selected preset folders from the current directory."""
        if not self.selected_folder:
            messagebox.showwarning(
                "Advertencia",
                "Por favor, selecciona una carpeta primero.",
            )
            return

        preset_name = self.preset_option.get()
        confirm = messagebox.askyesno(
            "Eliminar carpetas",
            f"¿Deseas eliminar las carpetas del preset '{preset_name}' en la carpeta seleccionada?"
        )
        if confirm:
            if self.organizer.delete_folder_structure(preset_name):
                self.refresh_view()

    def open_folder(self):
        """Open the selected folder in the file explorer."""
        if not self.selected_folder:
            messagebox.showwarning(
                "Advertencia",
                "Por favor, selecciona una carpeta primero.",
            )
            return

        try:
            if sys.platform == "win32":
                os.startfile(self.selected_folder)
            elif sys.platform == "darwin":
                subprocess.call(["open", self.selected_folder])
            else:
                subprocess.call(["xdg-open", self.selected_folder])
            self.add_log_message(f"📂 Carpeta abierta: {self.selected_folder}")
        except Exception as e:
            self.add_log_message(f"⚠️ No se pudo abrir la carpeta: {e}")

    def organize_files(self):
        """Organize files in selected folder."""
        if not self.selected_folder:
            messagebox.showwarning(
                "Advertencia",
                "Por favor, selecciona una carpeta primero.",
            )
            return

        # Confirm action
        response = messagebox.askyesno(
            "Confirmar",
            "¿Estás seguro de que deseas organizar los archivos?\n"
            "Esta acción moverá los archivos a sus carpetas correspondientes.",
        )

        if response:
            stats = self.organizer.organize_files()
            self.add_log_message(stats["summary"])
            self.refresh_view()

    def refresh_view(self):
        """Refresh the folder tree view."""
        if self.selected_folder:
            self.folder_tree.display_tree(self.selected_folder)
            self.add_log_message("📊 Vista actualizada")

    def add_log_message(self, message: str):
        """Update status label."""
        self.status_label.configure(text=message)

    def run(self):
        """Run the application."""
        self.app.mainloop()
