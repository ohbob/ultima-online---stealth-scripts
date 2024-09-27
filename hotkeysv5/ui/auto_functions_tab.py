import tkinter as tk
from tkinter import ttk

class AutoFunctionsTab(ttk.Frame):
    BUTTON_PADX = 5
    BUTTON_PADY = 5
    BUTTON_BG_ON = "sea green"
    BUTTON_BG_OFF = "light gray"
    BUTTON_FG_ON = "white"
    BUTTON_FG_OFF = "black"
    DEFAULT_TIMEOUT = "1000"
    TOGGLE_BUTTON_WIDTH = 10  # Set a fixed width for the toggle button

    def __init__(self, parent, main_controller):
        super().__init__(parent)
        self.main_controller = main_controller
        self.create_widgets()

    def create_widgets(self):
        self.tree = self.create_treeview()
        self.tree.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=self.BUTTON_PADX, pady=self.BUTTON_PADY)

        self.set_hotkey_button = self.create_button(button_frame, "Set Hotkey", self.set_hotkey)
        self.clear_hotkey_button = self.create_button(button_frame, "Clear Hotkey", self.clear_hotkey)
        self.run_once_button = self.create_button(button_frame, "Run Once", self.run_once)

        self.auto_var = tk.BooleanVar(value=False)
        self.toggle_auto_button = self.create_toggle_button(button_frame, "Auto: Off", self.toggle_auto_function, self.auto_var)

        ttk.Label(button_frame, text="Timeout:").pack(side=tk.RIGHT, padx=self.BUTTON_PADX)
        self.timeout_entry = ttk.Entry(button_frame, width=5)
        self.timeout_entry.pack(side=tk.RIGHT, padx=self.BUTTON_PADX)
        self.timeout_entry.insert(0, self.DEFAULT_TIMEOUT)
        self.timeout_entry.bind('<FocusOut>', self.update_timeout)

    def create_treeview(self):
        tree = ttk.Treeview(self, columns=('Script', 'V1', 'V2', 'V3', 'Hotkey', 'Enabled'), show='headings')
        for col in tree['columns']:
            tree.heading(col, text=col)
            tree.column(col, width=100 if col in ('Script', 'Hotkey') else 50)
        tree.tag_configure('enabled', background='lightgreen')
        tree.tag_configure('disabled', background='lightgray')
        return tree

    def create_button(self, parent, text, command):
        button = ttk.Button(parent, text=text, command=command)
        button.pack(side=tk.LEFT, padx=self.BUTTON_PADX)
        return button

    def create_toggle_button(self, parent, text, command, var):
        button = tk.Button(parent, text=text, command=command, 
                           bg=self.BUTTON_BG_OFF, fg=self.BUTTON_FG_OFF, 
                           relief=tk.RAISED, width=self.TOGGLE_BUTTON_WIDTH)
        button.pack(side=tk.RIGHT, padx=self.BUTTON_PADX)
        return button

    def set_hotkey(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            func_name = self.tree.item(item, 'values')[0]
            self.main_controller.set_hotkey(func_name)

    def clear_hotkey(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            func_name = self.tree.item(item, 'values')[0]
            self.main_controller.clear_hotkey(func_name)

    def run_once(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            func_name = self.tree.item(item, 'values')[0]
            timeout = int(self.timeout_entry.get())
            self.main_controller.set_auto_functions_timeout(timeout)
            self.main_controller.run_once(func_name)

    def toggle_auto_function(self):
        new_state = not self.auto_var.get()
        self.auto_var.set(new_state)
        self.update_toggle_button(self.toggle_auto_button, "Auto", new_state)
        self.main_controller.set_auto_functions_state(new_state)

    def update_toggle_button(self, button, label, state):
        button.config(
            text=f"{label}: {'On' if state else 'Off'}",
            bg=self.BUTTON_BG_ON if state else self.BUTTON_BG_OFF,
            fg=self.BUTTON_FG_ON if state else self.BUTTON_FG_OFF
        )

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        auto_functions = self.main_controller.get_auto_functions()
        for func_name, data in auto_functions.items():
            enabled = data.get('enabled', False)
            values = (func_name, data.get('variable1', ''), data.get('variable2', ''), 
                      data.get('variable3', ''), data.get('hotkey', ''), 'Yes' if enabled else 'No')
            tag = 'enabled' if enabled else 'disabled'
            self.tree.insert('', 'end', values=values, tags=(tag,))

    def update_enabled_status(self, func_name, enabled):
        for item in self.tree.get_children():
            if self.tree.item(item, 'values')[0] == func_name:
                self.tree.item(item, tags=('enabled' if enabled else 'disabled',))
                self.tree.set(item, 'Enabled', 'Yes' if enabled else 'No')
                break

    def update_timeout(self, event):
        timeout = self.timeout_entry.get()
        self.main_controller.set_auto_functions_timeout(timeout)