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
    TOGGLE_BUTTON_WIDTH = 10

    def __init__(self, parent, main_controller):
        super().__init__(parent)
        self.main_controller = main_controller
        self.create_widgets()

    def create_widgets(self):
        self.tree = self.create_treeview()
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Change the single-click binding to double-click
        self.tree.bind('<Double-1>', self.on_double_click)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=self.BUTTON_PADX, pady=self.BUTTON_PADY)

        self.set_hotkey_button = self.create_button(button_frame, "Set Hotkey", self.set_hotkey)
        self.clear_hotkey_button = self.create_button(button_frame, "Clear Hotkey", self.clear_hotkey)
        self.run_once_button = self.create_button(button_frame, "Run Once", self.run_once)

        # Replace text with arrow symbols for move up and down buttons
        self.move_up_button = self.create_button(button_frame, "↑", self.move_up)
        self.move_down_button = self.create_button(button_frame, "↓", self.move_down)

        self.auto_var = tk.BooleanVar(value=False)
        self.auto_text = tk.StringVar(value="Auto: Off")
        self.toggle_auto_button = tk.Button(button_frame, textvariable=self.auto_text, 
                                            command=self.toggle_auto_function, 
                                            width=self.TOGGLE_BUTTON_WIDTH)
        self.toggle_auto_button.pack(side=tk.RIGHT, padx=self.BUTTON_PADX)

        ttk.Label(button_frame, text="Timeout:").pack(side=tk.RIGHT, padx=self.BUTTON_PADX)
        self.timeout_entry = ttk.Entry(button_frame, width=5)
        self.timeout_entry.pack(side=tk.RIGHT, padx=self.BUTTON_PADX)
        self.timeout_entry.insert(0, self.DEFAULT_TIMEOUT)
        self.timeout_entry.bind('<FocusOut>', self.update_timeout)

        # Bind drag and drop events
        self.tree.bind('<ButtonPress-1>', self.on_press)
        self.tree.bind('<B1-Motion>', self.on_motion)
        self.tree.bind('<ButtonRelease-1>', self.on_release)

    def create_treeview(self):
        tree = ttk.Treeview(self, columns=('Order', 'Hotkey', 'Enabled'), show='tree headings')
        tree.heading('Order', text='Order')
        tree.heading('Hotkey', text='Hotkey')
        tree.heading('Enabled', text='Enabled')
        tree.column('#0', width=200)
        tree.column('Order', width=50)
        tree.column('Hotkey', width=100)
        tree.column('Enabled', width=50)
        tree.tag_configure('enabled', background='lightgreen')
        tree.tag_configure('disabled', background='lightgray')
        return tree

    def on_double_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            if column == '#3':  # Enabled column
                self.toggle_enabled(item)

    def toggle_enabled(self, item):
        func_name = self.tree.item(item, 'text')
        current_value = self.tree.set(item, 'Enabled')
        new_value = 'No' if current_value == 'Yes' else 'Yes'
        enabled = new_value == 'Yes'
        
        # Update the function state in the main controller
        self.main_controller.toggle_auto_function(func_name, enabled)
        
        # Update the tree view
        self.tree.set(item, 'Enabled', new_value)
        self.tree.item(item, tags=('enabled' if enabled else 'disabled',))

    def create_button(self, parent, text, command):
        button = ttk.Button(parent, text=text, command=command, width=2 if len(text) == 1 else None)
        button.pack(side=tk.LEFT, padx=self.BUTTON_PADX)
        return button

    def set_hotkey(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            func_name = self.tree.item(item, 'text')
            self.main_controller.set_hotkey(func_name)

    def clear_hotkey(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            func_name = self.tree.item(item, 'text')
            self.main_controller.clear_hotkey(func_name)

    def run_once(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            if not self.tree.get_children(item):  # Check if the item has no children (i.e., it's not a folder)
                func_name = self.tree.item(item, 'text')
                timeout = int(self.timeout_entry.get())
                self.main_controller.set_auto_functions_timeout(timeout)
                self.main_controller.run_auto_function(func_name, loop=False, timeout=timeout)
            else:
                print("Please select a script, not a folder.")
        else:
            print("Please select a script to run.")

    def toggle_auto_function(self):
        new_state = not self.auto_var.get()
        self.update_auto_button_state(new_state)
        self.main_controller.set_auto_functions_state(new_state)

    def update_auto_button_state(self, state):
        self.auto_var.set(state)
        self.auto_text.set(f"Auto: {'On' if state else 'Off'}")
        self.toggle_auto_button.config(
            bg=self.BUTTON_BG_ON if state else self.BUTTON_BG_OFF,
            fg=self.BUTTON_FG_ON if state else self.BUTTON_FG_OFF
        )

    def populate_tree(self):
        print("Populating Auto Functions tab tree...")
        self.tree.delete(*self.tree.get_children())
        auto_functions = self.main_controller.get_auto_functions()
        print(f"Found {len(auto_functions)} categories of auto functions")
        
        for category, functions in auto_functions.items():
            category_parts = category.split('.')
            if category_parts[0] == 'auto':
                category_parts = category_parts[1:]  # Remove 'auto' from the start
            
            parent = ''
            for i, part in enumerate(category_parts):
                full_path = '.'.join(category_parts[:i+1])
                if not self.tree.exists(full_path):
                    self.tree.insert(parent, 'end', full_path, text=part, open=True)
                parent = full_path

            print(f"Adding category: {'.'.join(category_parts)} with {len(functions)} functions")
            for func_name, func_data in functions.items():
                values = [
                    func_data.get('order', ''),
                    func_data.get('hotkey', ''),
                    'Yes' if func_data.get('enabled', False) else 'No'
                ]
                tag = 'enabled' if func_data.get('enabled', False) else 'disabled'
                self.tree.insert(parent, 'end', text=func_name, values=values, tags=(tag,))
        print("Auto Functions tab tree population complete")

    def move_up(self):
        selected = self.tree.selection()
        if selected:
            for item in selected:
                idx = self.tree.index(item)
                if idx > 0:
                    self.tree.move(item, self.tree.parent(item), idx-1)
            self.update_order()

    def move_down(self):
        selected = self.tree.selection()
        if selected:
            for item in reversed(selected):
                idx = self.tree.index(item)
                self.tree.move(item, self.tree.parent(item), idx+1)
            self.update_order()

    def update_order(self):
        for idx, item in enumerate(self.tree.get_children(), start=1):
            self.tree.set(item, 'Order', str(idx))
            func_name = self.tree.item(item, 'text')
            self.main_controller.update_auto_function_order(func_name, idx)
        self.main_controller.save_auto_functions()

    def update_enabled_status(self, func_name, enabled):
        for item in self.tree.get_children():
            if self.tree.item(item, 'text') == func_name:
                self.tree.item(item, tags=('enabled' if enabled else 'disabled',))
                self.tree.set(item, 'Enabled', 'Yes' if enabled else 'No')
                break

    def update_timeout(self, event):
        timeout = self.timeout_entry.get()
        self.main_controller.set_auto_functions_timeout(timeout)

    def on_press(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.drag_start_y = event.y
            self.drag_item = item

    def on_motion(self, event):
        if hasattr(self, 'drag_item'):
            moved_y = event.y - self.drag_start_y
            if abs(moved_y) >= 20:  # Threshold to start dragging
                target = self.tree.identify_row(event.y)
                if target and self.tree.parent(target) == self.tree.parent(self.drag_item):
                    self.tree.move(self.drag_item, self.tree.parent(self.drag_item), self.tree.index(target))
                    self.drag_start_y = event.y

    def on_release(self, event):
        if hasattr(self, 'drag_item'):
            del self.drag_item
            del self.drag_start_y
            self.update_order()