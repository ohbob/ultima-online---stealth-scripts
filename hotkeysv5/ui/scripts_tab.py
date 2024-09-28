import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

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
        self.parent = parent  # Store the parent widget
        self.create_widgets()
        self.current_hotkey = None
        self.listening_for_hotkey = False

    def create_widgets(self):
        self.tree = self.create_treeview()
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Add double-click binding
        self.tree.bind('<Double-1>', self.on_double_click)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=self.BUTTON_PADX, pady=self.BUTTON_PADY)

        # Replace the "Set Hotkey" button with a label and entry
        self.hotkey_frame = ttk.Frame(button_frame)
        self.hotkey_frame.pack(side=tk.LEFT, padx=self.BUTTON_PADX)

        self.hotkey_label = ttk.Label(self.hotkey_frame, text="Hotkey:")
        self.hotkey_label.pack(side=tk.LEFT)

        self.hotkey_entry = ttk.Entry(self.hotkey_frame, width=15)
        self.hotkey_entry.pack(side=tk.LEFT, padx=(0, self.BUTTON_PADX))
        self.hotkey_entry.bind('<KeyPress>', self.on_hotkey_keypress)
        self.hotkey_entry.bind('<KeyRelease>', self.on_hotkey_keyrelease)

        self.set_hotkey_button = ttk.Button(self.hotkey_frame, text="Set", command=self.set_hotkey)
        self.set_hotkey_button.pack(side=tk.LEFT)

        self.remove_button = self.create_button(button_frame, "Clear Hotkey", self.clear_hotkey)

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
            hotkey = simpledialog.askstring("Set Hotkey", "Enter hotkey combination:")
            if hotkey:
                self.main_controller.set_hotkey(func, hotkey)
                self.tree.set(item, 'Hotkey', hotkey)

    def remove_hotkey(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            func = self.tree.item(item, 'text').split(' (')[0]
            self.main_controller.remove_hotkey(func)
            self.tree.set(item, 'Hotkey', '')

    def launch_function(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            if self.tree.parent(item):  # Check if the selected item is not a folder
                func_name = self.tree.item(item, 'text')
                self.run_script(func_name)
            else:
                print("Please select a script, not a folder.")

    def toggle_loop_function(self):
        new_state = not self.loop_var.get()
        self.update_loop_button_state(new_state)
        if new_state:
            self.start_loop()
        else:
            self.stop_loop()

    def start_loop(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            if self.tree.parent(item):  # Check if the selected item is not a folder
                func_name = self.tree.item(item, 'text')
                timeout = int(self.timeout_entry.get())
                self.main_controller.scripts_controller.run_script(func_name, loop=True, timeout=timeout)
            else:
                print("Please select a script, not a folder.")
        else:
            print("Please select a script to run in a loop.")

    def stop_loop(self):
        self.main_controller.scripts_controller.stop_loop_execution()

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
            # Sort the functions alphabetically
            sorted_functions = sorted(functions.items(), key=lambda x: x[0].lower())
            for func_name, func_data in sorted_functions:
                hotkey = func_data.get('hotkey', '')
                self.tree.insert(parent, 'end', text=func_name, values=(hotkey,))
        print("Scripts tab tree population complete")
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

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

    def on_double_click(self, event):
        item = self.tree.identify('item', event.x, event.y)
        if self.tree.parent(item):  # Check if the clicked item is not a folder
            func_name = self.tree.item(item, 'text')
            self.run_script(func_name)

    def run_script(self, func_name):
        loop = self.loop_var.get()
        timeout = int(self.timeout_entry.get())
        self.main_controller.run_once(func_name)

    def toggle_hotkey_function(self):
        new_state = not self.hotkey_var.get()
        self.update_hotkey_button_state(new_state)
        self.main_controller.set_hotkeys_state(new_state)

    def run_once(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            func_name = self.tree.item(item, 'text')
            self.main_controller.run_once(func_name)

    def set_hotkey(self):
        selected = self.tree.selection()
        if selected and self.tree.parent(selected[0]):
            item = selected[0]
            func_name = self.tree.item(item, 'text')
            hotkey = self.hotkey_entry.get()
            if hotkey:
                self.main_controller.set_hotkey(hotkey, func_name)
                self.tree.set(item, 'Hotkey', hotkey)
                print(f"Hotkey '{hotkey}' set for function: {func_name}")
            else:
                print("Please enter a hotkey")
        else:
            print("Please select a script to set a hotkey.")

    def clear_hotkey(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            if self.tree.parent(item):  # Check if the selected item is not a folder
                func_name = self.tree.item(item, 'text')
                hotkey = self.tree.set(item, 'Hotkey')
                if hotkey:
                    self.main_controller.clear_hotkey(hotkey)
                    self.tree.set(item, 'Hotkey', '')
                    print(f"Hotkey cleared for function '{func_name}'")
                else:
                    print(f"No hotkey set for function '{func_name}'")
            else:
                print("Please select a script, not a folder.")
        else:
            print("Please select a script to clear its hotkey.")

    def update_hotkey_display(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            hotkey = self.tree.set(item, 'Hotkey')
            self.hotkey_entry.delete(0, tk.END)
            self.hotkey_entry.insert(0, hotkey if hotkey else "")

    def on_tree_select(self, event):
        self.update_hotkey_display()

    def on_hotkey_keypress(self, event):
        if event.keysym in ['Control_L', 'Control_R', 'Shift_L', 'Shift_R', 'Alt_L', 'Alt_R']:
            return 'break'  # Prevent these from being added to the entry
        
        modifiers = []
        if event.state & 0x4:
            modifiers.append('Ctrl')
        if event.state & 0x1:
            modifiers.append('Shift')
        if event.state & 0x8:
            modifiers.append('Alt')
        
        key = event.keysym
        hotkey = '+'.join(modifiers + [key])
        
        self.hotkey_entry.delete(0, tk.END)
        self.hotkey_entry.insert(0, hotkey)
        return 'break'  # Prevent default behavior

    def on_hotkey_keyrelease(self, event):
        return 'break'  # Prevent default behavior