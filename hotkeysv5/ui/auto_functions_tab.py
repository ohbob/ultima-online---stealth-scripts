import tkinter as tk
from tkinter import ttk

class AutoFunctionsTab(ttk.Frame):
    def __init__(self, parent, main_controller):
        super().__init__(parent)
        self.main_controller = main_controller
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=('Script', 'V1', 'V2', 'V3', 'Hotkey', 'Enabled'), show='headings')
        self.tree.heading('Script', text='Script')
        self.tree.heading('V1', text='V1')
        self.tree.heading('V2', text='V2')
        self.tree.heading('V3', text='V3')
        self.tree.heading('Hotkey', text='Hotkey')
        self.tree.heading('Enabled', text='Enabled')
        self.tree.column('Script', width=150)
        self.tree.column('V1', width=50)  # Half of the original width
        self.tree.column('V2', width=50)  # Half of the original width
        self.tree.column('V3', width=50)  # Half of the original width
        self.tree.column('Hotkey', width=100)
        self.tree.column('Enabled', width=50)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.tag_configure('enabled', background='lightgreen')
        self.tree.tag_configure('disabled', background='lightgray')

        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        self.add_button = ttk.Button(button_frame, text="Add Hotkey", command=self.add_hotkey)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = ttk.Button(button_frame, text="Remove Hotkey", command=self.remove_hotkey)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.run_once_button = ttk.Button(button_frame, text="Run Once", command=self.run_once)
        self.run_once_button.pack(side=tk.LEFT, padx=5)

        ttk.Label(button_frame, text="Timeout:").pack(side=tk.LEFT, padx=5)
        self.timeout_entry = ttk.Entry(button_frame, width=5)
        self.timeout_entry.pack(side=tk.LEFT, padx=5)
        self.timeout_entry.insert(0, "1000")  # Default timeout value

        self.toggle_button = ttk.Button(button_frame, text="Auto: Off", command=self.toggle_auto_function, style="Toggle.TButton")
        self.toggle_button.pack(side=tk.RIGHT, padx=5)  # Move to the right side

        # Create a style for the toggle button
        style = ttk.Style()
        style.configure("Toggle.TButton", foreground="gray")

    def add_hotkey(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            func_name = self.tree.item(item, 'values')[0]  # Get the script name from the first column
            self.main_controller.add_hotkey(func_name)

    def remove_hotkey(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            func_name = self.tree.item(item, 'values')[0]  # Get the script name from the first column
            self.main_controller.remove_hotkey(func_name)

    def run_once(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            func_name = self.tree.item(item, 'values')[0]  # Get the script name from the first column
            self.main_controller.run_once(func_name)

    def toggle_auto_function(self):
        enabled = self.main_controller.toggle_all_auto_functions()
        self.update_toggle_button(enabled)

    def update_toggle_button(self, enabled=None):
        if enabled is None:
            enabled = self.main_controller.are_auto_functions_enabled()
        self.toggle_button.config(text=f"Auto: {'On' if enabled else 'Off'}")
        self.toggle_button.config(style="ToggleOn.TButton" if enabled else "ToggleOff.TButton")

        # Update the style for the toggle button
        style = ttk.Style()
        style.configure("ToggleOn.TButton", foreground="green")
        style.configure("ToggleOff.TButton", foreground="gray")

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        auto_functions = self.main_controller.get_auto_functions()
        for func_name, data in auto_functions.items():
            enabled = data.get('enabled', False)
            var1 = data.get('variable1', '')
            var2 = data.get('variable2', '')
            var3 = data.get('variable3', '')
            hotkey = data.get('hotkey', '')
            tag = 'enabled' if enabled else 'disabled'
            self.tree.insert('', 'end', values=(func_name, var1, var2, var3, hotkey, 'Yes' if enabled else 'No'), tags=(tag,))

    def update_enabled_status(self, func_name, enabled):
        for item in self.tree.get_children():
            if self.tree.item(item, 'values')[0] == func_name:  # Check the script name in the first column
                self.tree.item(item, tags=('enabled' if enabled else 'disabled',))
                self.tree.set(item, 'Enabled', 'Yes' if enabled else 'No')
                break