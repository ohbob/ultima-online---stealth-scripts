import tkinter as tk
from tkinter import ttk

class AutoFunctionsTab:
    def __init__(self, notebook, manager):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Auto Functions")
        self.manager = manager
        
       

        # Create the treeview with updated column order
        self.tree = ttk.Treeview(self.frame, columns=('Function', 'Variable1', 'Variable2', 'Variable3', 'Hotkey', 'Enabled'), show='headings')
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Define column headings and widths
        self.tree.heading('Function', text='Function')
        self.tree.heading('Variable1', text='V1')
        self.tree.heading('Variable2', text='V2')
        self.tree.heading('Variable3', text='V3')
        self.tree.heading('Hotkey', text='Hotkey')
        self.tree.heading('Enabled', text='Enabled')

        self.tree.column('Function', width=200, anchor='w')  # Increased width
        self.tree.column('Variable1', width=40, anchor='center')  # Reduced width
        self.tree.column('Variable2', width=40, anchor='center')  # Reduced width
        self.tree.column('Variable3', width=40, anchor='center')  # Reduced width
        self.tree.column('Hotkey', width=100, anchor='center')
        self.tree.column('Enabled', width=80, anchor='center')

        # Create tag configurations for enabled/disabled indicators
        self.enabled_image = self.create_circle('green')
        self.disabled_image = self.create_circle('red')
        self.tree.tag_configure('enabled', image=self.enabled_image, background='#E6FFE6')  # Light green background
        self.tree.tag_configure('disabled', image=self.disabled_image)  # Removed background for disabled items

        # Bind events for drag and drop
        self.tree.bind('<ButtonPress-1>', self.on_press)
        self.tree.bind('<B1-Motion>', self.on_motion)
        self.tree.bind('<ButtonRelease-1>', self.on_release)

        # Bind double-click event to edit variables or toggle enabled state
        self.tree.bind('<Double-1>', self.on_double_click)

        # Add a toggle button for auto functions with padding
        self.toggle_button = ttk.Button(self.frame, text="Enable Auto Functions", command=self.toggle_auto_functions)
        self.toggle_button.pack(pady=5, padx=10, anchor='e', side='right')

        # Initialize the button state
        self.update_toggle_button()

    def create_circle(self, color):
        canvas = tk.Canvas(self.frame, width=15, height=15, highlightthickness=0)
        canvas.create_oval(2, 2, 13, 13, fill=color, outline="")
        return canvas

    def load_auto_functions(self, auto_functions):
        self.tree.delete(*self.tree.get_children())  # Clear existing items
        for func_name, data in auto_functions.items():
            enabled = data.get('enabled', False)
            var1 = data.get('variable1', '')
            var2 = data.get('variable2', '')
            var3 = data.get('variable3', '')
            hotkey = data.get('hotkey', '')
            tag = 'enabled' if enabled else 'disabled'
            self.tree.insert('', 'end', values=(func_name, var1, var2, var3, hotkey, 'True' if enabled else 'False'), tags=(tag,))

    def on_double_click(self, event):
        item = self.tree.identify('item', event.x, event.y)
        column = self.tree.identify('column', event.x, event.y)
        if column in ['#2', '#3', '#4']:  # Variable columns
            self.edit_variable(item, int(column[1])-1)
        elif column == '#6':  # Enabled column
            self.toggle_enabled(item)

    def edit_variable(self, item, var_index):
        column = f'Variable{var_index}'
        value = self.tree.set(item, column)
        
        # Get the bounding box of the cell
        bbox = self.tree.bbox(item, column)
        
        if not bbox:  # If bbox is None, the item might not be visible
            self.tree.see(item)  # Ensure the item is visible
            bbox = self.tree.bbox(item, column)
        
        # Create a style for borderless entry
        style = ttk.Style()
        style.configure("Borderless.TEntry", borderwidth=0, relief="flat")
        
        # Create and place the entry widget with the borderless style
        entry = ttk.Entry(self.tree, justify='center', style="Borderless.TEntry")
        entry.insert(0, value)
        entry.select_range(0, tk.END)
        entry.focus()
        
        entry.bind('<Return>', lambda e: self.save_variable(item, entry, var_index))
        entry.bind('<Escape>', lambda e: self.cancel_edit(entry))
        
        # Place the entry widget in the correct position
        entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
        
        # Store the entry widget to remove it later
        self.current_edit = entry

    def save_variable(self, item, entry, var_index):
        value = entry.get()
        column = f'Variable{var_index}'
        self.tree.set(item, column, value)
        func_name = self.tree.item(item, 'values')[0]
        self.manager.update_auto_function_variable(func_name, var_index, value)
        self.cancel_edit(entry)
        self.manager.debug(f"Updated {func_name} variable {var_index} to: {value}", "info")  # Add this debug line

    def cancel_edit(self, entry):
        entry.destroy()
        if hasattr(self, 'current_edit'):
            del self.current_edit

    def toggle_enabled(self, item):
        func_name = self.tree.item(item, 'values')[0]
        current_state = self.tree.item(item, 'tags')[0] == 'enabled'
        new_state = not current_state
        self.manager.toggle_auto_function(func_name)
        self.update_enabled_status(func_name, new_state)

    def update_enabled_status(self, func_name, enabled):
        for item in self.tree.get_children():
            if self.tree.item(item, 'values')[0] == func_name:
                tag = 'enabled' if enabled else 'disabled'
                self.tree.item(item, tags=(tag,))
                self.tree.set(item, 'Enabled', 'True' if enabled else 'False')
                break

    # Add methods for adding, editing, and removing auto functions as needed

    def on_press(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.drag_start_y = event.y
            self.drag_item = item

    def on_motion(self, event):
        if hasattr(self, 'drag_item'):
            moved_y = event.y - self.drag_start_y
            if abs(moved_y) >= 20:  # Adjust this value to change drag sensitivity
                target = self.tree.identify_row(event.y)
                if target and target != self.drag_item:
                    self.tree.move(self.drag_item, self.tree.parent(target), self.tree.index(target))
                    self.drag_start_y = event.y

    def on_release(self, event):
        if hasattr(self, 'drag_item'):
            del self.drag_item
            del self.drag_start_y
            self.manager.update_auto_function_order(self.get_function_order())

    def get_function_order(self):
        return [self.tree.item(child)['values'][0] for child in self.tree.get_children('')]

    def toggle_auto_functions(self):
        self.manager.toggle_all_auto_functions()
        self.update_toggle_button()

    def update_toggle_button(self):
        if self.manager.auto_functions_enabled:
            self.toggle_button.config(text="Disable Auto Functions")
        else:
            self.toggle_button.config(text="Enable Auto Functions")

    # ... (keep other methods as they are)