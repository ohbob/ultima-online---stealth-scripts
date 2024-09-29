import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import logging

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
        self.logger = logging.getLogger(__name__)
        self.logger.info("ScriptsTab initialized")

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
                self.main_controller.save_hotkeys()

    def remove_hotkey(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            func = self.tree.item(item, 'text').split(' (')[0]
            self.main_controller.remove_hotkey(func)
            self.tree.set(item, 'Hotkey', '')
            self.main_controller.save_hotkeys()

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
                self.main_controller.run_script_in_thread(func_name, loop=True, timeout=timeout)
            else:
                print("Please select a script, not a folder.")
        else:
            print("Please select a script to run in a loop.")

    def stop_loop(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            if self.tree.parent(item):  # Check if the selected item is not a folder
                func_name = self.tree.item(item, 'text')
                self.main_controller.stop_script(func_name)
            else:
                print("Please select a script, not a folder.")
        else:
            print("Please select a script to stop its loop.")

    def update_timeout(self, event):
        timeout = self.timeout_entry.get()
        self.main_controller.set_scripts_timeout(timeout)

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        discovered_functions = self.main_controller.get_discovered_functions()
        hotkeys = self.main_controller.hotkey_controller.get_hotkeys()
        
        print(f"Discovered functions: {discovered_functions}")
        print(f"Hotkeys: {hotkeys}")
        
        for category, functions in discovered_functions.items():
            category_parts = category.split('.')
            parent = ''
            for i, part in enumerate(category_parts):
                category_id = '.'.join(category_parts[:i+1])
                if not self.tree.exists(category_id):
                    self.tree.insert(parent, 'end', category_id, text=part)
                parent = category_id
            
            for func_name in functions:
                hotkey = hotkeys.get(func_name, '')
                print(f"Inserting function: {func_name}, hotkey: {hotkey}")
                self.tree.insert(parent, 'end', text=func_name, values=(hotkey,))

        self.update_hotkeys_display(hotkeys)
        print(f"Populated tree with {len(hotkeys)} hotkeys")

    def update_hotkeys_display(self, hotkeys):
        # Reverse the hotkeys dictionary to map function names to hotkeys
        func_to_hotkey = {v: k for k, v in hotkeys.items()}
        
        def update_item(item):
            # Check if the item is a function (leaf node) and not a category (parent node)
            if not self.tree.get_children(item):  # If the item has no children, it's a function
                func_name = self.tree.item(item, 'text').strip()
                hotkey = func_to_hotkey.get(func_name, '')
                print(f"Updating item: {item}, func_name: {func_name}, hotkey: {hotkey}")
                self.tree.set(item, 'Hotkey', hotkey)
            else:
                # If the item is a category, recursively update its children
                for child in self.tree.get_children(item):
                    update_item(child)

        # Start updating from the root items
        for item in self.tree.get_children():
            update_item(item)

        print(f"Updated hotkeys display with {len(hotkeys)} hotkeys")

    # Remove the refresh_ui method if it's not being used elsewhere

    def update_loop_button_state(self, state):
        self.loop_var.set(state)
        self.loop_text.set(f"Loop: {'On' if state else 'Off'}")
        self.toggle_loop_button.config(
            bg=self.BUTTON_BG_ON if state else self.BUTTON_BG_OFF,
            fg=self.BUTTON_FG_ON if state else self.BUTTON_FG_OFF
        )

    def update_hotkey_button_state(self, state):
        self.logger.info(f"Updating hotkey button state: {state}")
        self.hotkey_var.set(state)
        self.hotkey_text.set(f"Hotkey: {'On' if state else 'Off'}")
        self.toggle_hotkey_button.config(
            bg=self.BUTTON_BG_ON if state else self.BUTTON_BG_OFF,
            fg=self.BUTTON_FG_ON if state else self.BUTTON_FG_OFF
        )
        print(f"Hotkey button state updated: {'On' if state else 'Off'}")

    def on_double_click(self, event):
        item = self.tree.identify('item', event.x, event.y)
        if self.tree.parent(item):  # Check if the clicked item is not a folder
            func_name = self.tree.item(item, 'text')
            self.run_script(func_name)

    def run_script(self, func_name):
        loop = self.loop_var.get()
        timeout = int(self.timeout_entry.get())
        if loop:
            self.main_controller.run_script_in_thread(func_name, loop=True, timeout=timeout)
        else:
            self.main_controller.run_once(func_name)

    def toggle_hotkey_function(self):
        self.logger.info("toggle_hotkey_function called")
        new_state = self.main_controller.toggle_all_hotkeys()
        self.update_hotkey_button_state(new_state)

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
                self.populate_tree()
                print(f"Hotkey '{hotkey}' set for function: {func_name}")
            else:
                print("Please enter a hotkey")
        else:
            print("Please select a script to set a hotkey.")

    def clear_hotkey(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            if self.tree.parent(item):
                func_name = self.tree.item(item, 'text')
                hotkey = self.tree.set(item, 'Hotkey')
                if hotkey:
                    self.main_controller.clear_hotkey(hotkey)
                    self.tree.set(item, 'Hotkey', '')
                    self.populate_tree()
                    print(f"Hotkey cleared for function '{func_name}'")
                else:
                    print(f"No hotkey set for function '{func_name}'")
            else:
                print("Please select a script, not a folder.")
        else:
            print("Please select a script to clear its hotkey.")

    def update_hotkey_display(self, hotkeys):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add hotkeys to the treeview
        for hotkey, func_name in hotkeys.items():
            self.tree.insert('', 'end', text=func_name, values=(hotkey,))

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

    def toggle_hotkeys(self):
        current_state = self.main_controller.state.hotkeys_enabled
        new_state = not current_state
        self.main_controller.set_hotkeys_state(new_state)
        self.update_hotkey_button_state(new_state)