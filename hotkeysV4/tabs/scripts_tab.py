import tkinter as tk
from tkinter import ttk, messagebox

class ScriptsTab:
    def __init__(self, notebook, manager):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Scripts")
        self.manager = manager

        self.tree = ttk.Treeview(self.frame, columns=('Function', 'Hotkey'), show='tree headings')
        self.tree.heading('Function', text='Function')
        self.tree.heading('Hotkey', text='Hotkey')
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=5, padx=10, fill=tk.X)

        ttk.Button(button_frame, text="Assign", command=self.assign_hotkey).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove", command=self.remove_hotkey).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Launch", command=self.launch_function).pack(side=tk.LEFT, padx=5)

        # Loop functionality
        self.loop_var = tk.BooleanVar()
        ttk.Checkbutton(button_frame, text="Loop", variable=self.loop_var, command=self.toggle_loop).pack(side=tk.LEFT, padx=5)
        ttk.Label(button_frame, text="Delay (ms):").pack(side=tk.LEFT, padx=5)
        self.loop_delay = tk.StringVar(value="1000")
        ttk.Entry(button_frame, textvariable=self.loop_delay, width=5).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="Save", command=self.manager.save_config).pack(side=tk.LEFT, padx=5)

        self.tree.bind('<Double-1>', self.on_double_click)

    def load_hotkeys(self, hotkeys, system_functions, regular_functions):
        self.tree.delete(*self.tree.get_children())  # Clear existing items
        
        # Create "System Functions" section
        system_id = self.tree.insert('', 'end', text='System Functions', open=True)
        for func_name in system_functions:
            display_name = ' '.join(func_name.split('_')).title()
            self.tree.insert(system_id, 'end', values=(func_name, hotkeys.get(func_name, '')))

        # Create "Scripts" section
        scripts_id = self.tree.insert('', 'end', text='Scripts', open=True)
        for func_name in regular_functions:
            self.tree.insert(scripts_id, 'end', values=(func_name, hotkeys.get(func_name, '')))

    def assign_hotkey(self):
        selected = self.tree.selection()
        if selected:
            self.manager.assign_hotkey(selected[0], self.tree)

    # Remove the on_hotkey_press method

    def remove_hotkey(self):
        selected = self.tree.selection()
        if selected:
            self.manager.remove_hotkey(selected[0], self.tree)

    def launch_function(self):
        self.manager.launch_selected_function()

    def run_selected_function(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a function to run.")
            return
        func = self.tree.item(selected[0])['values'][0]
        print(f"Running function: {func}")
        if self.loop_var.get():
            self.start_loop(func)
        else:
            self.manager.activate_function(func)

    def toggle_loop(self):
        if self.loop_var.get():
            selected = self.tree.selection()
            if selected:
                func = self.tree.item(selected[0])['values'][0]
                self.start_loop(func)
        else:
            self.stop_loop()

    def start_loop(self, func):
        delay = int(self.loop_delay.get())
        self.loop_id = self.manager.master.after(delay, self.loop_function, func)

    def loop_function(self, func):
        self.manager.activate_function(func)
        if self.loop_var.get():
            delay = int(self.loop_delay.get())
            self.loop_id = self.manager.master.after(delay, self.loop_function, func)

    def stop_loop(self):
        if hasattr(self, 'loop_id'):
            self.manager.master.after_cancel(self.loop_id)

    def on_double_click(self, event):
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if not item:
            return
        
        if column == '#2':  # Hotkey column
            self.assign_hotkey(item)