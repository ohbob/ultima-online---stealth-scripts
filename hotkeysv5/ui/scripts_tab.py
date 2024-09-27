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
        self.toggle_hotkey_button = self.create_toggle_button(button_frame, "Hotkey: Off", self.toggle_hotkey_function, self.hotkey_var)



        self.loop_var = tk.BooleanVar(value=False)
        self.toggle_loop_button = self.create_toggle_button(button_frame, "Loop: Off", self.toggle_loop_function, self.loop_var)


        ttk.Label(button_frame, text="Timeout:").pack(side=tk.RIGHT, padx=self.BUTTON_PADX)
        self.timeout_entry = ttk.Entry(button_frame, width=5)
        self.timeout_entry.pack(side=tk.RIGHT, padx=self.BUTTON_PADX)
        self.timeout_entry.insert(0, self.DEFAULT_TIMEOUT)
        self.timeout_entry.bind('<FocusOut>', self.update_timeout)

        self.launch_button = self.create_button(button_frame, "Run Once", self.launch_function)
        self.launch_button.pack(side=tk.RIGHT, padx=self.BUTTON_PADX)



    def create_treeview(self):
        tree = ttk.Treeview(self, columns=('Script', 'Hotkey'), show='headings')
        tree.heading('Script', text='Script')
        tree.heading('Hotkey', text='Hotkey')
        tree.column('Script', width=200)
        tree.column('Hotkey', width=100)
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
            func = self.tree.item(item, 'text').split(' (')[0]
            loop = self.loop_var.get()
            timeout = int(self.timeout_entry.get())
            self.main_controller.set_scripts_timeout(timeout)
            self.main_controller.launch_function(func, loop, timeout)

    def toggle_loop_function(self):
        new_state = not self.loop_var.get()
        self.loop_var.set(new_state)
        self.update_toggle_button(self.toggle_loop_button, "Loop", new_state)
        self.main_controller.set_loop_state(new_state)

    def toggle_hotkey_function(self):
        new_state = not self.hotkey_var.get()
        self.hotkey_var.set(new_state)
        self.update_toggle_button(self.toggle_hotkey_button, "Hotkey", new_state)
        self.main_controller.set_hotkeys_state(new_state)

    def update_toggle_button(self, button, label, state):
        button.config(
            text=f"{label}: {'On' if state else 'Off'}",
            bg=self.BUTTON_BG_ON if state else self.BUTTON_BG_OFF,
            fg=self.BUTTON_FG_ON if state else self.BUTTON_FG_OFF
        )

    def update_timeout(self, event):
        timeout = self.timeout_entry.get()
        self.main_controller.set_scripts_timeout(timeout)

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        discovered_functions = self.main_controller.get_discovered_functions()
        hotkeys = self.main_controller.get_hotkeys()
        
        for category, functions in discovered_functions.items():
            category_id = self.tree.insert('', 'end', values=(category, ''))
            for func_name in functions:
                hotkey = hotkeys.get(func_name, '')
                self.tree.insert(category_id, 'end', values=(func_name, hotkey))

    # Add other script tab-related methods