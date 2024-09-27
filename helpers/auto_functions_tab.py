import tkinter as tk
from tkinter import ttk

class AutoFunctionsTab:
    def __init__(self, notebook, manager):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Auto Functions")
        self.manager = manager

        self.tree = ttk.Treeview(self.frame, columns=('Name', 'Var1', 'Var2', 'Var3', 'Hotkey', 'Enabled'), show='headings')
        self.tree.heading('Name', text='Function Name')
        self.tree.heading('Var1', text='Variable 1')
        self.tree.heading('Var2', text='Variable 2')
        self.tree.heading('Var3', text='Variable 3')
        self.tree.heading('Hotkey', text='Hotkey')
        self.tree.heading('Enabled', text='Enabled')
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.tree.bind('<Double-1>', self.on_double_click)

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=5, padx=10, fill=tk.X)

        ttk.Button(button_frame, text="Add", command=self.add_auto_function).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove", command=self.remove_auto_function).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit", command=self.edit_auto_function).pack(side=tk.LEFT, padx=5)
        self.toggle_button = ttk.Button(button_frame, text="Toggle All Auto Functions", command=self.toggle_all_auto_functions)
        self.toggle_button.pack(side=tk.LEFT, padx=5)

        self.var1_entry = ttk.Entry(button_frame)
        self.var1_entry.pack(side=tk.LEFT, padx=5)
        self.var2_entry = ttk.Entry(button_frame)
        self.var2_entry.pack(side=tk.LEFT, padx=5)
        self.var3_entry = ttk.Entry(button_frame)
        self.var3_entry.pack(side=tk.LEFT, padx=5)

    def on_double_click(self, event):
        item = self.tree.identify('item', event.x, event.y)
        if item:
            self.toggle_enabled(item)

    def toggle_all_auto_functions(self):
        new_state = self.manager.toggle_auto_functions()
        self.update_toggle_button()

    def update_toggle_button(self):
        if self.manager.auto_functions_enabled:
            self.toggle_button.config(text="Disable All Auto Functions")
        else:
            self.toggle_button.config(text="Enable All Auto Functions")

    def toggle_enabled(self, item):
        func_name = self.tree.item(item, 'values')[0]
        self.manager.toggle_auto_function(func_name)
        self.update_enabled_status(func_name, self.manager.auto_functions[func_name]['enabled'])

    def update_enabled_status(self, func_name, enabled):
        for item in self.tree.get_children():
            if self.tree.item(item, 'values')[0] == func_name:
                values = list(self.tree.item(item, 'values'))
                values[5] = str(enabled)
                self.tree.item(item, values=values)
                break

    def add_auto_function(self):
        # Implement the logic to add a new auto function
        pass

    def remove_auto_function(self):
        selected = self.tree.selection()
        if selected:
            func_name = self.tree.item(selected[0], 'values')[0]
            del self.manager.auto_functions[func_name]
            self.tree.delete(selected[0])
            self.manager.save_config()

    def edit_auto_function(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            func_name = self.tree.item(item, 'values')[0]
            var1 = self.var1_entry.get()
            var2 = self.var2_entry.get()
            var3 = self.var3_entry.get()
            
            self.manager.auto_functions[func_name]['variable1'] = var1
            self.manager.auto_functions[func_name]['variable2'] = var2
            self.manager.auto_functions[func_name]['variable3'] = var3
            
            values = list(self.tree.item(item, 'values'))
            values[1] = var1
            values[2] = var2
            values[3] = var3
            self.tree.item(item, values=values)
            
            self.manager.save_config()

    def populate_tree(self, auto_functions):
        self.tree.delete(*self.tree.get_children())
        for func_name, func_data in auto_functions.items():
            enabled = func_data.get('enabled', False)
            var1 = func_data.get('variable1', '')
            var2 = func_data.get('variable2', '')
            var3 = func_data.get('variable3', '')
            hotkey = func_data.get('hotkey', '')
            self.tree.insert('', 'end', values=(func_name, var1, var2, var3, hotkey, str(enabled)))