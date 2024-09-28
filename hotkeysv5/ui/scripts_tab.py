import tkinter as tk
from tkinter import ttk

class ScriptsTab(ttk.Frame):
    BUTTON_PADX = 5
    BUTTON_PADY = 5
    BUTTON_BG_ON = "sea green"
    BUTTON_BG_OFF = "light gray"
    BUTTON_FG_ON = "white"
    BUTTON_FG_OFF = "black"
    DEFAULT_TIMEOUT = "1000"
    TOGGLE_BUTTON_WIDTH = 10  # Set a fixed width for the toggle buttons


    def __init__(self, parent, main_controller):
        super().__init__(parent)
        self.main_controller = main_controller
        self.create_widgets()

    def create_widgets(self):
        self.tree = self.create_treeview()
        self.tree.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=self.BUTTON_PADX, pady=self.BUTTON_PADY)

        self.add_button = self.create_button(button_frame, "Set Hotkey", self.add_hotkey)
        self.remove_button = self.create_button(button_frame, "Clear Hotkey", self.remove_hotkey)






        self.hotkey_var = tk.BooleanVar(value=False)
        self.hotkey_text = tk.StringVar(value="Hotkey: Off")
        self.toggle_hotkey_button = tk.Button(button_frame, textvariable=self.hotkey_text, 
                                              command=self.toggle_hotkey_function, 
                                              width=self.TOGGLE_BUTTON_WIDTH)
        self.toggle_hotkey_button.pack(side=tk.RIGHT, padx=self.BUTTON_PADX)



        self.loop_var = tk.BooleanVar(value=False)
        self.loop_text = tk.StringVar(value="Loop: Off")
        self.toggle_loop_button = tk.Button(button_frame, textvariable=self.loop_text, 
                                            command=self.toggle_loop_function, 
                                            width=self.TOGGLE_BUTTON_WIDTH)
        self.toggle_loop_button.pack(side=tk.RIGHT, padx=self.BUTTON_PADX)


        ttk.Label(button_frame, text="Timeout:").pack(side=tk.RIGHT, padx=self.BUTTON_PADX)
        self.timeout_entry = ttk.Entry(button_frame, width=5)
        self.timeout_entry.pack(side=tk.RIGHT, padx=self.BUTTON_PADX)
        self.timeout_entry.insert(0, self.DEFAULT_TIMEOUT)
        self.timeout_entry.bind('<FocusOut>', self.update_timeout)

        self.launch_button = self.create_button(button_frame, "Run Once", self.launch_function)
        self.launch_button.pack(side=tk.RIGHT, padx=self.BUTTON_PADX)



    def create_treeview(self):
        tree = ttk.Treeview(self, columns=('Hotkey',), show='tree headings')
        tree.heading('Hotkey', text='Hotkey')
        tree.column('Hotkey', width=100)
        tree.column('#0', width=200)  # Width for the tree structure column
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
            if self.tree.parent(item):  # Check if the selected item is not a folder
                func_name = self.tree.item(item, 'text')
                loop = self.loop_var.get()
                timeout = int(self.timeout_entry.get())
                self.main_controller.set_scripts_timeout(timeout)
                self.main_controller.run_script(func_name, loop, timeout)
            else:
                print("Please select a script, not a folder.")

    def toggle_loop_function(self):
        new_state = not self.loop_var.get()
        self.update_loop_button_state(new_state)
        self.main_controller.set_loop_state(new_state)

    def toggle_hotkey_function(self):
        new_state = not self.hotkey_var.get()
        self.update_hotkey_button_state(new_state)
        self.main_controller.set_hotkeys_state(new_state)

    def update_timeout(self, event):
        timeout = self.timeout_entry.get()
        self.main_controller.set_scripts_timeout(timeout)

    def populate_tree(self):
        print("Populating Scripts tab tree...")
        self.tree.delete(*self.tree.get_children())
        discovered_functions = self.main_controller.get_discovered_functions()
        print(f"Found {len(discovered_functions)} categories of functions")
        
        for category, functions in discovered_functions.items():
            category_parts = category.split('.')
            if category_parts[0] == 'functions':
                category_parts = category_parts[1:]  # Remove 'functions' from the start
            
            parent = ''
            for i, part in enumerate(category_parts):
                full_path = '.'.join(category_parts[:i+1])
                if not self.tree.exists(full_path):
                    self.tree.insert(parent, 'end', full_path, text=part, open=True)
                parent = full_path

            print(f"Adding category: {'.'.join(category_parts)} with {len(functions)} functions")
            for func_name, func_data in functions.items():
                hotkey = func_data.get('hotkey', '')
                self.tree.insert(parent, 'end', text=func_name, values=(hotkey,))
        print("Scripts tab tree population complete")

    # Remove the refresh_ui method if it's not being used elsewhere

    def update_loop_button_state(self, state):
        self.loop_var.set(state)
        self.loop_text.set(f"Loop: {'On' if state else 'Off'}")
        self.toggle_loop_button.config(
            bg=self.BUTTON_BG_ON if state else self.BUTTON_BG_OFF,
            fg=self.BUTTON_FG_ON if state else self.BUTTON_FG_OFF
        )

    def update_hotkey_button_state(self, state):
        self.hotkey_var.set(state)
        self.hotkey_text.set(f"Hotkey: {'On' if state else 'Off'}")
        self.toggle_hotkey_button.config(
            bg=self.BUTTON_BG_ON if state else self.BUTTON_BG_OFF,
            fg=self.BUTTON_FG_ON if state else self.BUTTON_FG_OFF
        )