"""UI components for GestorCarpetas."""

import customtkinter as ctk
import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import constants
from constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    THEME,
    APPEARANCE_MODE,
    FILE_ICONS,
    PRESET_STRUCTURES,
    PRESET_DESCRIPTIONS,
    OTROS_FOLDER,
    DEFAULT_ICON,
)
from file_organizer import FileOrganizer
from custom_extensions import CustomExtensionsManager, get_extensions_manager


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
            height=30,
        )
        scrollbar.configure(command=self.tree.yview)
        self.tree.pack(side="left", fill="both", expand=True)

        # Configure style
        style = ttk.Style()
        style.theme_use("clam")

        self.tree.heading("#0", text="Estructura de Carpetas")
        self.tree.column("#0", width=760)

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
        from constants import EXTENSIONES
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
            fg_color="#2563EB",
            hover_color="#1D4ED8",
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
            background="#FFFFFF",
            foreground="#0F172A",
            fieldbackground="#FFFFFF",
            borderwidth=0
        )
        style.map('Treeview', background=[('selected', '#DBEAFE')])

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
            fg_color="#EF4444",
            hover_color="#DC2626",
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
            text="✅ Aplicar estructura",
            command=self.apply_structure,
            height=40,
        )
        apply_button.pack(side="left", fill="x", expand=True, padx=(0, 6))

        delete_preset_button = ctk.CTkButton(
            bottom_frame,
            text="🗑️ Eliminar preset",
            command=self.delete_preset,
            fg_color="#EF4444",
            hover_color="#DC2626",
            height=40,
            width=160,
        )
        delete_preset_button.pack(side="left", padx=(0, 6))

        close_button = ctk.CTkButton(
            bottom_frame,
            text="Cerrar",
            command=self.destroy,
            fg_color="#64748B",
            hover_color="#475569",
            height=40,
            width=100,
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

    def delete_preset(self):
        """Delete the currently selected preset from the list (does NOT touch the disk)."""
        preset_name = self.preset_option.get() if hasattr(self, 'preset_option') else ""

        if not preset_name or preset_name in ("Nuevo preset", "(Sin presets)"):
            messagebox.showwarning("Advertencia", "Selecciona un preset del menú para poder eliminarlo.")
            return

        confirm = messagebox.askyesno(
            "Eliminar preset",
            f"¿Deseas eliminar el preset '{preset_name}' de la lista?\n"
            "Esta acción NO borra ninguna carpeta del disco.",
        )
        if not confirm:
            return

        # Remove from dicts
        self.presets.pop(preset_name, None)
        self.descriptions.pop(preset_name, None)

        # Refresh dropdown
        remaining = list(self.presets.keys())
        if remaining:
            self.preset_option.configure(values=remaining)
            self.select_preset(remaining[0])
        else:
            self.preset_option.configure(values=["(Sin presets)"])
            self.preset_option.set("(Sin presets)")
            self.folder_list = []
            self.refresh_preview()

        # Notify parent UI so its dropdown also updates
        if self.on_preset_saved:
            self.on_preset_saved(remaining[0] if remaining else "")

        messagebox.showinfo("Listo", f"Preset '{preset_name}' eliminado de la lista.")

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


class CustomExtensionsEditor(ctk.CTkToplevel):
    """Popup window to manage custom file extensions."""

    def __init__(self, parent, on_save=None):
        super().__init__(parent)
        self.title("Administrador de Extensiones Personalizadas")
        self.geometry("600x500")
        self.resizable(True, True)
        self.attributes("-topmost", True)
        self.transient(parent)
        self.on_save = on_save
        
        # Use the singleton so changes persist across the app
        self.manager = get_extensions_manager()
        # Reload from disk to catch any changes made externally
        self.manager.load_extensions()
        self._create_widgets()
        self.refresh_categories_list()

    def _create_widgets(self):
        """Create UI widgets."""
        # Title
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(
            title_frame,
            text="Administrador de Extensiones Personalizadas",
            font=("Arial", 14, "bold"),
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text="Define tus propias categorías y extensiones de archivo",
            font=("Arial", 10),
            text_color="gray",
        ).pack(anchor="w", pady=(0, 5))

        # Main content frame
        content_frame = ctk.CTkFrame(self)
        content_frame.pack(fill="both", expand=True, padx=15, pady=10)
        content_frame.grid_rowconfigure(0, weight=0)  # add section
        content_frame.grid_rowconfigure(1, weight=0)  # label
        content_frame.grid_rowconfigure(2, weight=1)  # listbox expands
        content_frame.grid_rowconfigure(3, weight=0)  # buttons
        content_frame.grid_columnconfigure(0, weight=1)

        # Section 1: Add new extension
        add_frame = ctk.CTkFrame(content_frame)
        add_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        add_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            add_frame,
            text="Agregar Nueva Categoría",
            font=("Arial", 11, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        # Category name input
        ctk.CTkLabel(add_frame, text="Nombre de la carpeta:", font=("Arial", 10)).pack(anchor="w")
        self.category_entry = ctk.CTkEntry(
            add_frame,
            placeholder_text="Ej: Diseño, Proyectos, etc.",
            height=32,
        )
        self.category_entry.pack(fill="x", pady=(3, 8))

        # Extensions input
        ctk.CTkLabel(add_frame, text="Extensiones (separadas por comas):", font=("Arial", 10)).pack(anchor="w")
        self.extensions_entry = ctk.CTkEntry(
            add_frame,
            placeholder_text="Ej: .psd, .ai, .xd  (se agregarán automáticamente los puntos)",
            height=32,
        )
        self.extensions_entry.pack(fill="x", pady=(3, 8))
        self.extensions_entry.bind("<Return>", lambda e: self.add_category())

        add_button = ctk.CTkButton(
            add_frame,
            text="➕ Agregar Categoría",
            command=self.add_category,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            height=35,
        )
        add_button.pack(fill="x")

        # Section 2: Existing categories
        ctk.CTkLabel(
            content_frame,
            text="Categorías Personalizadas",
            font=("Arial", 11, "bold"),
        ).grid(row=1, column=0, sticky="ew", pady=(15, 8))

        # List frame with scrollbar
        list_frame = ctk.CTkFrame(content_frame)
        list_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 15))
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.categories_listbox = tk.Listbox(
            list_frame,
            height=8,
            yscrollcommand=scrollbar.set,
            font=("Courier", 9),
            bg="#f0f0f0",
            relief="flat",
            borderwidth=0,
        )
        scrollbar.configure(command=self.categories_listbox.yview)
        self.categories_listbox.pack(side="left", fill="both", expand=True)
        self.categories_listbox.bind("<<ListboxSelect>>", self.on_category_select)

        # Action buttons frame
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.grid(row=3, column=0, sticky="ew")
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=0)

        delete_button = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Eliminar Seleccionada",
            command=self.delete_category,
            fg_color="#EF4444",
            hover_color="#DC2626",
            height=35,
        )
        delete_button.pack(side="left", fill="x", expand=True, padx=(0, 5))

        # Bottom buttons
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=15, pady=(0, 15))
        bottom_frame.grid_columnconfigure(0, weight=1)

        close_button = ctk.CTkButton(
            bottom_frame,
            text="Cerrar",
            command=self.close_window,
            fg_color="#64748B",
            hover_color="#475569",
            height=35,
            width=120,
        )
        close_button.pack(side="right", padx=(5, 0))

        info_label = ctk.CTkLabel(
            bottom_frame,
            text="",
            font=("Arial", 10),
            text_color="gray",
        )
        info_label.pack(side="left", fill="x", expand=True)
        self.info_label = info_label

    def add_category(self):
        """Add a new custom category."""
        category_name = self.category_entry.get().strip()
        extensions_text = self.extensions_entry.get().strip()

        if not category_name:
            messagebox.showwarning("Advertencia", "Por favor ingresa un nombre para la categoría.")
            return

        if not extensions_text:
            messagebox.showwarning("Advertencia", "Por favor ingresa al menos una extensión.")
            return

        # Validate category name
        if not self.manager.validate_category_name(category_name):
            messagebox.showerror(
                "Error",
                "El nombre contiene caracteres inválidos. Usa solo letras, números, guiones y espacios."
            )
            return

        # Parse extensions
        extensions = [ext.strip() for ext in extensions_text.split(",")]
        extensions = [ext for ext in extensions if ext]  # Remove empty strings

        # Add category
        if self.manager.add_extension(category_name, extensions):
            self.category_entry.delete(0, "end")
            self.extensions_entry.delete(0, "end")
            self.refresh_categories_list()
            self.info_label.configure(
                text=f"✅ Categoría '{category_name}' agregada con {len(extensions)} extensión(es)"
            )
            if self.on_save:
                self.on_save()
        else:
            messagebox.showerror("Error", "No se pudo agregar la categoría. Verifica los datos.")

    def delete_category(self):
        """Delete selected category."""
        selection = self.categories_listbox.curselection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una categoría para eliminar.")
            return

        index = selection[0]
        categories = list(self.manager.get_all_categories().keys())
        if index < len(categories):
            category_name = categories[index]
            
            confirm = messagebox.askyesno(
                "Confirmar",
                f"¿Deseas eliminar la categoría '{category_name}' y todas sus extensiones?"
            )
            
            if confirm:
                if self.manager.remove_category(category_name):
                    self.refresh_categories_list()
                    self.info_label.configure(text=f"✅ Categoría '{category_name}' eliminada")
                    
                    if self.on_save:
                        self.on_save()

    def on_category_select(self, event):
        """Handle category selection."""
        selection = self.categories_listbox.curselection()
        if selection:
            index = selection[0]
            categories = list(self.manager.get_all_categories().keys())
            if index < len(categories):
                category_name = categories[index]
                extensions = self.manager.get_extensions_for_category(category_name)
                self.info_label.configure(
                    text=f"Categoría: {category_name} • Extensiones: {', '.join(extensions)}"
                )

    def refresh_categories_list(self):
        """Refresh the categories listbox."""
        self.categories_listbox.delete(0, tk.END)
        custom_categories = self.manager.get_all_categories()
        
        if not custom_categories:
            self.categories_listbox.insert(tk.END, "(No hay categorías personalizadas)")
            self.info_label.configure(text="Crea tu primera categoría personalizada arriba")
        else:
            for category, extensions in sorted(custom_categories.items()):
                display_text = f"📁 {category:20} → {', '.join(extensions)}"
                self.categories_listbox.insert(tk.END, display_text)

    def close_window(self):
        """Close the window."""
        self.destroy()


class GestorCarpetasUI:
    """Main UI class for GestorCarpetas."""

    def __init__(self):
        # Setup appearance
        ctk.set_appearance_mode(APPEARANCE_MODE)
        ctk.set_default_color_theme(THEME)

        # Create main window
        self.app = ctk.CTk()
        self.app.configure(fg_color="#F8FAFC")
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
        main_container.pack(fill="both", expand=True, padx=12, pady=12)

        # Main content area
        content_frame = ctk.CTkFrame(main_container)
        content_frame.pack(fill="both", expand=True, pady=(0, 10))
        content_frame.grid_columnconfigure(0, weight=3, uniform="panel")
        content_frame.grid_columnconfigure(1, weight=1, uniform="panel")
        content_frame.grid_rowconfigure(0, weight=1)

        # Left panel - Folder tree
        left_panel = ctk.CTkFrame(content_frame)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 0))

        title_tree = ctk.CTkLabel(
            left_panel,
            text="🌳 Explorador de Carpetas",
            font=("Arial", 16, "bold"),
        )
        title_tree.pack(anchor="w", padx=12, pady=(12, 8))

        self.folder_tree = FolderTreeView(left_panel)
        self.folder_tree.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        # Right panel - Status and options
        right_panel = ctk.CTkFrame(content_frame)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=(0, 0))
        right_panel.grid_rowconfigure(3, weight=1)

        # 1. Folder Selection
        folder_frame = ctk.CTkFrame(right_panel)
        folder_frame.pack(fill="x", padx=12, pady=(12, 8))
        
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
            text_color="#64748B",
            wraplength=360,
            justify="left",
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
            fg_color="#2563EB",
            hover_color="#1D4ED8",
        )
        button_organize.pack(fill="x", pady=(0, 5))

        button_open_folder = ctk.CTkButton(
            action_frame,
            text="📂 Abrir en Explorador",
            command=self.open_folder,
            height=35,
            fg_color="#3B82F6",
            hover_color="#2563EB",
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
            wraplength=360,
            justify="left",
            text_color="gray",
        )
        self.preset_description.pack(anchor="w", pady=(0, 5))

        categories_label = ctk.CTkLabel(
            struct_frame,
            text="Categorías a organizar",
            font=("Arial", 11, "bold"),
        )
        categories_label.pack(anchor="w", pady=(10, 5))

        self.category_list = list(constants.EXTENSIONES.keys()) + [OTROS_FOLDER]

        button_create_structure = ctk.CTkButton(
            struct_frame,
            text="✅ Crear Estructura de Carpetas",
            command=self.create_structure,
            fg_color="#60A5FA",
            hover_color="#3B82F6",
            text_color="white",
            height=35,
        )
        button_create_structure.pack(fill="x", pady=(0, 5))

        button_manage_presets = ctk.CTkButton(
            struct_frame,
            text="⚙️ Administrar Presets",
            command=self.open_preset_editor,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            height=35,
        )
        button_manage_presets.pack(fill="x", pady=(0, 5))

        button_manage_extensions = ctk.CTkButton(
            struct_frame,
            text="📝 Extensiones Personalizadas",
            command=self.open_extensions_manager,
            fg_color="#7C3AED",
            hover_color="#6D28D9",
            height=35,
        )
        button_manage_extensions.pack(fill="x", pady=(0, 5))

        button_delete_folders = ctk.CTkButton(
            struct_frame,
            text="🗑️ Eliminar Carpetas Vacías",
            command=self.delete_structure,
            fg_color="#EF4444",
            hover_color="#DC2626",
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
            width=180,
        )
        button_refresh.pack(side="left", padx=5, pady=5)
        
        self.status_label = ctk.CTkLabel(
            bottom_bar,
            text="Listo",
            text_color="#64748B",
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

    def open_extensions_manager(self):
        """Open the custom extensions manager window."""
        CustomExtensionsEditor(
            self.app,
            on_save=self.on_custom_extensions_saved,
        )

    def on_custom_extensions_saved(self):
        """Callback when custom extensions are saved."""
        # Force the singleton to reload from disk
        from custom_extensions import get_extensions_manager
        get_extensions_manager().load_extensions()
        self.add_log_message("✅ Extensiones personalizadas actualizadas. Se usarán en la próxima organización.")

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

    def get_selected_categories(self) -> list[str]:
        """Return the list of current categories to organize."""
        from constants import get_extensiones
        return list(get_extensiones().keys()) + [OTROS_FOLDER]

    def organize_files(self):
        """Organize files in selected folder."""
        if not self.selected_folder:
            messagebox.showwarning(
                "Advertencia",
                "Por favor, selecciona una carpeta primero.",
            )
            return

        selected_categories = self.get_selected_categories()
        if not selected_categories:
            messagebox.showwarning(
                "Advertencia",
                "Selecciona al menos una categoría para organizar.",
            )
            return

        response = messagebox.askyesno(
            "Confirmar",
            "¿Estás seguro de que deseas organizar los archivos?\n"
            "Esta acción moverá los archivos a sus carpetas correspondientes.",
        )

        if response:
            stats = self.organizer.organize_files(categories=selected_categories)
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
        try:
            self.app.mainloop()
        except KeyboardInterrupt:
            pass
