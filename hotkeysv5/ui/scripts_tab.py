import tkinter as tk
from tkinter import ttk

class ScriptsTab(ttk.Frame):
    def __init__(self, parent, main_controller):
        super().__init__(parent)
        self.main_controller = main_controller
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=('Hotkey',), show='tree headings')
        self.tree.heading('Hotkey', text='Hotkey')
        self.tree.column('Hotkey', width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        self.add_button = ttk.Button(button_frame, text="Add Hotkey", command=self.add_hotkey)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = ttk.Button(button_frame, text="Remove Hotkey", command=self.remove_hotkey)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.launch_button = ttk.Button(button_frame, text="Launch Function", command=self.launch_function)
        self.launch_button.pack(side=tk.LEFT, padx=5)

        # Add loop toggle button
        self.loop_var = tk.BooleanVar()
        self.loop_button = ttk.Button(button_frame, text="Loop: Off", command=self.toggle_loop)
        self.loop_button.pack(side=tk.LEFT, padx=5)

        ttk.Label(button_frame, text="Timeout:").pack(side=tk.LEFT, padx=5)
        self.timeout_entry = ttk.Entry(button_frame, width=5)
        self.timeout_entry.pack(side=tk.LEFT, padx=5)
        self.timeout_entry.insert(0, "1000")  # Default timeout value

        # Move Toggle Hotkeys button to the right
        self.toggle_hotkeys_button = ttk.Button(button_frame, text="Hotkeys: Off", command=self.toggle_hotkeys, style="Toggle.TButton")
        self.toggle_hotkeys_button.pack(side=tk.RIGHT, padx=5)

        # Create a style for the toggle button
        style = ttk.Style()
        style.configure("Toggle.TButton", foreground="gray")

    def add_hotkey(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            func = self.tree.item(item, 'text')
            self.main_controller.assign_hotkey(func, self.tree)

    def remove_hotkey(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            func = self.tree.item(item, 'text').split(' (')[0]
            self.main_controller.remove_hotkey(func, self.tree)

    def launch_function(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            func = self.tree.item(item, 'text').split(' (')[0]
            loop = self.loop_var.get()
            timeout = int(self.timeout_entry.get())
            self.main_controller.launch_function(func, loop, timeout)

    def toggle_loop(self):
        self.loop_var.set(not self.loop_var.get())
        self.loop_button.config(text=f"Loop: {'On' if self.loop_var.get() else 'Off'}")

    def toggle_hotkeys(self):
        enabled = self.main_controller.toggle_all_hotkeys()
        self.toggle_hotkeys_button.config(text=f"Hotkeys: {'On' if enabled else 'Off'}")
        self.toggle_hotkeys_button.config(style="ToggleOn.TButton" if enabled else "ToggleOff.TButton")

        # Update the style for the toggle button
        style = ttk.Style()
        style.configure("ToggleOn.TButton", foreground="green")
        style.configure("ToggleOff.TButton", foreground="gray")

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        discovered_functions = self.main_controller.get_discovered_functions()
        hotkeys = self.main_controller.get_hotkeys()
        
        for category, functions in discovered_functions.items():
            category_id = self.tree.insert('', 'end', text=category)
            for func_name in functions:
                hotkey = hotkeys.get(func_name, '')
                display_text = f"{func_name} ({hotkey})" if hotkey else func_name
                self.tree.insert(category_id, 'end', text=display_text)

    # Add other script tab-related methods