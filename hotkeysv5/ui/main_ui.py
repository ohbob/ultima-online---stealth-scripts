import tkinter as tk
from tkinter import ttk, messagebox
from .scripts_tab import ScriptsTab
from .auto_functions_tab import AutoFunctionsTab
from .friends_tab import FriendsTab
from .pets_tab import PetsTab

class MainUI:
    def __init__(self, root, main_controller):
        self.root = root
        self.main_controller = main_controller
        self.root.title("Hotkey Manager v5")
        self.create_widgets()
        self.main_controller.discover_all_functions()  

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.scripts_tab = ScriptsTab(self.notebook, self.main_controller)
        self.auto_functions_tab = AutoFunctionsTab(self.notebook, self.main_controller)
        self.friends_tab = FriendsTab(self.notebook, self.main_controller)
        self.pets_tab = PetsTab(self.notebook, self.main_controller)

        self.notebook.add(self.scripts_tab, text="Scripts")
        self.notebook.add(self.auto_functions_tab, text="Auto Functions")
        self.notebook.add(self.friends_tab, text="Friends")
        self.notebook.add(self.pets_tab, text="Pets")

    def populate_tree_views(self):
        self.scripts_tab.populate_tree()
        self.auto_functions_tab.populate_tree()
        self.friends_tab.populate_list()
        self.pets_tab.populate_list()

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def show_info(self, message):
        messagebox.showinfo("Information", message)

    def show_warning(self, message):
        messagebox.showwarning("Warning", message)

    def update_hotkeys_button(self, state):
        # This method should update the existing hotkeys button in the appropriate tab
        pass

    def update_auto_functions_button(self, state):
        # This method should update the existing auto functions button in the appropriate tab
        pass