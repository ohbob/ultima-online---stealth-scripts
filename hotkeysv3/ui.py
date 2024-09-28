import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from utils import debug
from py_stealth import *

class HotkeyConfigUI:
    def __init__(self, master, config):
        self.master = master
        self.config = config
        self.function_configs = {}
        self.loop_interval = tk.StringVar(value="500")  # Default loop interval
        self.friends = []
        self.pets = []
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_functions_tab()
        self.create_auto_functions_tab()
        self.create_friendlist_tab()
        self.create_petlist_tab()

    def create_functions_tab(self):
        self.functions_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.functions_frame, text="Functions")

        self.tree = ttk.Treeview(self.functions_frame, columns=('Function', 'Hotkey'), show='headings')
        self.tree.heading('Function', text='Function')
        self.tree.heading('Hotkey', text='Hotkey')
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.tree.bind('<Double-1>', self.on_double_click)

        button_frame = ttk.Frame(self.functions_frame)
        button_frame.pack(pady=5, padx=10, fill=tk.X)

        ttk.Button(button_frame, text="Assign", command=self.assign_hotkey).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove", command=self.remove_hotkey).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Run", command=self.run_selected_function).pack(side=tk.LEFT, padx=5)
        self.loop_var = tk.BooleanVar()
        ttk.Checkbutton(button_frame, text="Loop", variable=self.loop_var, command=self.toggle_loop).pack(side=tk.LEFT, padx=5)
        ttk.Label(button_frame, text="Interval (ms):").pack(side=tk.LEFT, padx=5)
        ttk.Entry(button_frame, textvariable=self.loop_interval, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save", command=self.save_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Enable/Disable All", command=self.toggle_all_hotkeys).pack(side=tk.LEFT, padx=5)

    def on_double_click(self, event):
        item = self.tree.identify('item', event.x, event.y)
        if item:
            self.assign_hotkey(item)

    def assign_hotkey(self, item=None):
        if item is None:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a function.")
                return
            item = selected[0]
        self.config.assign_hotkey(item, self.tree)

    def remove_hotkey(self):
        selected = self.tree.selection()
        if selected:
            self.config.remove_hotkey(selected[0], self.tree)

    def run_selected_function(self):
        selected = self.tree.selection()
        if selected:
            func_name = self.tree.item(selected[0])['values'][0]
            self.config.activate_function(func_name)

    def toggle_loop(self):
        # Implement loop functionality here
        pass

    def save_config(self):
        self.config.save_config()

    def toggle_all_hotkeys(self):
        self.config.toggle_all_hotkeys()

    def create_auto_functions_tab(self):
        self.auto_functions_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.auto_functions_frame, text="Auto Functions")

        self.config_tree = ttk.Treeview(self.auto_functions_frame, columns=('Function', 'Enabled', 'Threshold', 'Hotkey'), show='headings')
        self.config_tree.heading('Function', text='Function')
        self.config_tree.heading('Enabled', text='Enabled')
        self.config_tree.heading('Threshold', text='Threshold')
        self.config_tree.heading('Hotkey', text='Hotkey')
        self.config_tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.config_tree.bind('<Double-1>', self.on_config_double_click)

        button_frame = ttk.Frame(self.auto_functions_frame)
        button_frame.pack(pady=5, padx=10, fill=tk.X)

        ttk.Button(button_frame, text="Assign Hotkey", command=self.assign_auto_hotkey).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Hotkey", command=self.remove_auto_hotkey).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save", command=self.config.save_config).pack(side=tk.LEFT, padx=5)

    def create_friendlist_tab(self):
        self.friends_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.friends_frame, text="Friends")

        self.friends_tree = ttk.Treeview(self.friends_frame, columns=('ID', 'Name'), show='headings')
        self.friends_tree.heading('ID', text='Friend ID')
        self.friends_tree.heading('Name', text='Friend Name')
        self.friends_tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(self.friends_frame)
        button_frame.pack(pady=5, padx=10, fill=tk.X)

        ttk.Button(button_frame, text="Add", command=self.add_friend).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove", command=self.remove_friend).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save", command=self.save_friends).pack(side=tk.LEFT, padx=5)

    def create_petlist_tab(self):
        self.pets_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.pets_frame, text="Pets")

        self.pets_tree = ttk.Treeview(self.pets_frame, columns=('ID', 'Name'), show='headings')
        self.pets_tree.heading('ID', text='Pet ID')
        self.pets_tree.heading('Name', text='Pet Name')
        self.pets_tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(self.pets_frame)
        button_frame.pack(pady=5, padx=10, fill=tk.X)

        ttk.Button(button_frame, text="Add", command=self.add_pet).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove", command=self.remove_pet).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save", command=self.save_pets).pack(side=tk.LEFT, padx=5)

    def add_friend(self):
        debug("Please select a friend in the game.", "info")
        friend_id = self.getTargetID()
        if friend_id:
            friend_name = GetName(friend_id)
            self.friends.append((friend_id, friend_name))
            self.friends_tree.insert('', 'end', values=(friend_id, friend_name))
            debug(f"Added friend: {friend_name} (ID: {friend_id})", "success")
        else:
            debug("Failed to get friend ID.", "error")

    def remove_friend(self):
        selected = self.friends_tree.selection()
        if selected:
            friend_id, friend_name = self.friends_tree.item(selected[0])['values']
            self.friends = [f for f in self.friends if f[0] != friend_id]
            self.friends_tree.delete(selected[0])
            debug(f"Removed friend: {friend_name} (ID: {friend_id})", "info")

    def save_friends(self):
        self.config.config['friends'] = self.friends
        self.config.save_config()
        messagebox.showinfo("Friends", "Friends list saved successfully!")

    def add_pet(self):
        debug("Please select a pet in the game.", "info")
        pet_id = self.getTargetID()
        if pet_id:
            pet_name = GetName(pet_id)
            self.pets.append((pet_id, pet_name))
            self.pets_tree.insert('', 'end', values=(pet_id, pet_name))
            debug(f"Added pet: {pet_name} (ID: {pet_id})", "success")
        else:
            debug("Failed to get pet ID.", "error")

    def remove_pet(self):
        selected = self.pets_tree.selection()
        if selected:
            pet_id, pet_name = self.pets_tree.item(selected[0])['values']
            self.pets = [p for p in self.pets if p[0] != pet_id]
            self.pets_tree.delete(selected[0])
            debug(f"Removed pet: {pet_name} (ID: {pet_id})", "info")

    def save_pets(self):
        self.config.config['pets'] = self.pets
        self.config.save_config()
        messagebox.showinfo("Pets", "Pets list saved successfully!")

    def create_function_config(self, func_name, module):
        try:
            debug(f"Creating config for {func_name}", "info")
            enabled = self.config.config.get(func_name, {}).get('enabled', False)
            threshold = self.config.config.get(func_name, {}).get('threshold', 70)
            hotkey = self.config.config.get(func_name, {}).get('hotkey', '')

            self.function_configs[func_name] = {
                'enabled': tk.BooleanVar(value=enabled),
                'threshold': tk.StringVar(value=str(threshold)),
                'hotkey': tk.StringVar(value=hotkey),
                'function': getattr(module, 'example_autofunction', None)
            }

            item = self.config_tree.insert('', 'end', values=(func_name, 'Yes' if enabled else 'No', threshold, hotkey))

            enabled_checkbutton = ttk.Checkbutton(self.config_tree, variable=self.function_configs[func_name]['enabled'], command=lambda: self.update_function_config(func_name))
            threshold_entry = ttk.Entry(self.config_tree, textvariable=self.function_configs[func_name]['threshold'], width=10)
            threshold_entry.bind('<FocusOut>', lambda e: self.finish_edit(e, func_name))

            self.config_tree.set(item, 'Enabled', 'Yes' if enabled else 'No')
            self.config_tree.set(item, 'Threshold', str(threshold))
            self.config_tree.set(item, 'Hotkey', hotkey)

            self.config_tree.update()
            bbox = self.config_tree.bbox(item, 'Enabled')
            if bbox:
                enabled_checkbutton.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
            
            bbox = self.config_tree.bbox(item, 'Threshold')
            if bbox:
                threshold_entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])

            debug(f"Created config for {func_name} with enabled={enabled}, threshold={threshold}, and hotkey={hotkey}", "info")
        except Exception as e:
            debug(f"Error creating config for {func_name}: {str(e)}", "fail")

    def toggle_enabled(self, func_name):
        config = self.function_configs[func_name]
        config['enabled'].set(not config['enabled'].get())
        self.update_function_config(func_name)

    def on_config_double_click(self, event):
        item = self.config_tree.identify('item', event.x, event.y)
        column = self.config_tree.identify_column(event.x)
        
        if not item:
            return
        
        func_name = self.config_tree.item(item, 'values')[0]
        config = self.function_configs.get(func_name)
        
        if not config:
            return
        
        if column == '#2':  # Enabled column
            self.toggle_enabled(func_name)
        elif column == '#3':  # Threshold column
            self.edit_threshold(item, func_name)
        elif column == '#4':  # Hotkey column
            self.config.assign_hotkey(item, tree=self.config_tree)

    def edit_threshold(self, item, func_name):
        config = self.function_configs[func_name]
        entry = ttk.Entry(self.config_tree, textvariable=config['threshold'])
        entry.bind('<Return>', lambda e: self.finish_edit(e, func_name))
        entry.bind('<FocusOut>', lambda e: self.finish_edit(e, func_name))
        
        bbox = self.config_tree.bbox(item, '#3')
        if bbox:
            entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
        else:
            debug(f"Failed to get bbox for Threshold column of item {item}", "warning")
        entry.focus_set()

    def finish_edit(self, event, func_name):
        event.widget.destroy()
        self.update_function_config(func_name)

    def update_function_config(self, func_name):
        config = self.function_configs[func_name]
        enabled = config['enabled'].get()
        threshold = config['threshold'].get()
        hotkey = config['hotkey'].get()
        func = config['function']

        self.config.config[func_name] = {
            'enabled': enabled,
            'threshold': float(threshold),
            'hotkey': hotkey
        }

        item_id = self.config_tree.selection()[0]
        self.config_tree.item(item_id, values=(func_name, 'Yes' if enabled else 'No', threshold, hotkey))

        debug(f"Updated config for {func_name} with enabled={enabled}, threshold={threshold}, and hotkey={hotkey}", "info")

    def getTargetID(self):
        ClientRequestObjectTarget()
        WaitForClientTargetResponse(60000)
        if ClientTargetResponsePresent():
            response = ClientTargetResponse()
            if isinstance(response, dict):
                item_id = response.get('ID', None)
                return item_id
        return None

    def assign_auto_hotkey(self):
        selected = self.config_tree.selection()
        if not selected:
            debug("Please select an auto function.", "warning")
            return
        self.config.assign_hotkey(selected[0], tree=self.config_tree)

    def remove_auto_hotkey(self):
        selected = self.config_tree.selection()
        if not selected:
            debug("Please select an auto function.", "warning")
            return
        func_name = self.config_tree.item(selected[0])['values'][0]
        self.function_configs[func_name]['hotkey'].set('')
        self.config_tree.set(selected[0], 'Hotkey', '')
        self.update_function_config(func_name)
