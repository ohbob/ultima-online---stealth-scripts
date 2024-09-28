import json
import tkinter as tk
from tkinter import ttk, messagebox
import inspect
from pynput.keyboard import Key, KeyCode
from utils import debug, configurable_function, SystemFunctions
import game_functions  # Add this import at the top of the file

def load_config():
    try:
        with open('hotkey_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("No hotkey configuration found. Please set up hotkeys and save.")
        return {}

def parse_hotkey(hotkey_str):
    keys = hotkey_str.lower().split('+')
    parsed = []
    for key in keys:
        if key == '<ctrl>':
            parsed.append(Key.ctrl)
        elif key == '<alt>':
            parsed.append(Key.alt)
        elif key == '<shift>':
            parsed.append(Key.shift)
        elif key == '<grave>':
            parsed.append(KeyCode.from_char('`'))
        elif key.startswith('<') and key.endswith('>'):
            parsed.append(KeyCode.from_char(key[1:-1]))
        else:
            parsed.append(KeyCode.from_char(key))
    return tuple(parsed)

class HotkeyConfig:
    def __init__(self, master):
        self.master = master
        self.master.title("Hotkey Configuration")

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.hotkeys_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.hotkeys_frame, text="Hotkeys")

        self.tree = ttk.Treeview(self.hotkeys_frame, columns=('Function', 'Hotkey'), show='headings')
        self.tree.heading('Function', text='Function')
        self.tree.heading('Hotkey', text='Hotkey')
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.tree.bind('<Double-1>', self.on_double_click)

        button_frame = ttk.Frame(self.hotkeys_frame)
        button_frame.pack(pady=5, padx=10, fill=tk.X)

        ttk.Button(button_frame, text="Assign Hotkey", command=self.assign_hotkey).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Hotkey", command=self.remove_hotkey).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save", command=self.save_config).pack(side=tk.LEFT, padx=5)

        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text="Function Config")

        self.function_vars = {}  # Store tkinter variables for each function
        self.load_functions()
        self.load_config()

        # Start a periodic update
        self.update_ui()

    def load_functions(self):
        for func_name, func in inspect.getmembers(SystemFunctions, predicate=inspect.isfunction):
            if not func_name.startswith('__'):
                self.tree.insert('', 'end', values=(func_name, ''), tags=('system',))
        
        for func_name, func in inspect.getmembers(game_functions, predicate=inspect.isfunction):
            if not func_name.startswith('__') and func_name != 'main_loop':
                self.tree.insert('', 'end', values=(func_name, ''))
                if hasattr(func, 'config'):
                    self.create_function_config(func_name, func.config)

        self.tree.tag_configure('system', background='light gray')

    def create_function_config(self, func_name, config):
        frame = ttk.LabelFrame(self.config_frame, text=func_name)
        frame.pack(pady=5, padx=10, fill=tk.X)

        self.function_vars[func_name] = {}

        for param, default in config.items():
            if isinstance(default, bool):
                var = tk.BooleanVar(value=default)
                checkbutton = ttk.Checkbutton(frame, text=param, variable=var)
                checkbutton.pack(anchor=tk.W)
                self.function_vars[func_name][param] = var
            elif isinstance(default, (int, float)):
                var = tk.DoubleVar(value=default)
                ttk.Label(frame, text=f"{param}:").pack(side=tk.LEFT)
                ttk.Entry(frame, textvariable=var, width=10).pack(side=tk.LEFT, padx=5)
                self.function_vars[func_name][param] = var
            else:
                var = tk.StringVar(value=str(default))
                ttk.Label(frame, text=f"{param}:").pack(side=tk.LEFT)
                ttk.Entry(frame, textvariable=var).pack(side=tk.LEFT, padx=5)
                self.function_vars[func_name][param] = var

    def update_ui(self):
        for func_name, vars in self.function_vars.items():
            for param, var in vars.items():
                if hasattr(game_functions.Functions, func_name):
                    func = getattr(game_functions.Functions, func_name)
                    if hasattr(func, 'config') and param in func.config:
                        current_value = getattr(game_functions.Functions, f"{func_name}_{param}", None)
                        if current_value is not None and var.get() != current_value:
                            var.set(current_value)

        # Schedule the next update
        self.master.after(100, self.update_ui)  # Update every 100ms

    def load_config(self):
        try:
            with open('hotkey_config.json', 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {}

        for func, data in self.config.items():
            for item in self.tree.get_children():
                if self.tree.item(item)['values'][0] == func:
                    hotkey = data.get('hotkey', '') if isinstance(data, dict) else data
                    self.tree.item(item, values=(func, hotkey))
                    if hasattr(game_functions, func):
                        func_obj = getattr(game_functions, func)
                        if hasattr(func_obj, 'config'):
                            for param, value in data.items() if isinstance(data, dict) else {}:
                                if param != 'hotkey':
                                    var = getattr(self, f"{func}_{param}", None)
                                    if var:
                                        var.set(value)
                    break

    def save_config(self):
        self.config = {}
        for item in self.tree.get_children():
            func, hotkey = self.tree.item(item)['values']
            if hotkey:
                self.config[func] = {"hotkey": hotkey}

        for func_name, func in inspect.getmembers(game_functions, predicate=inspect.isfunction):
            if hasattr(func, 'config'):
                if func_name not in self.config:
                    self.config[func_name] = {}
                elif isinstance(self.config[func_name], str):
                    self.config[func_name] = {"hotkey": self.config[func_name]}
                for param in func.config:
                    var = getattr(self, f"{func_name}_{param}", None)
                    if var:
                        self.config[func_name][param] = var.get()

        with open('hotkey_config.json', 'w') as f:
            json.dump(self.config, f)
        messagebox.showinfo("Success", "Configuration saved successfully!")

        # Update the UI after saving
        self.update_ui()

    def assign_hotkey(self, item=None):
        if item is None:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a function.")
                return
            item = selected[0]

        func = self.tree.item(item)['values'][0]
        self.master.title(f"Press hotkey for {func}")
        self.current_hotkey = []
        self.current_item = item
        self.master.bind('<KeyPress>', self.on_keypress)
        self.master.bind('<KeyRelease>', self.on_keyrelease)

    def on_keypress(self, event):
        key = self.get_key_string(event)
        if key not in self.current_hotkey:
            self.current_hotkey.append(key)

    def on_keyrelease(self, event):
        if len(self.current_hotkey) > 0:
            hotkey = '+'.join(self.current_hotkey)
            func = self.tree.item(self.current_item)['values'][0]
            self.tree.item(self.current_item, values=(func, hotkey))
            self.master.title("Hotkey Configuration")
            self.master.unbind('<KeyPress>')
            self.master.unbind('<KeyRelease>')

    def get_key_string(self, event):
        key = event.keysym.lower()
        if key in ['control_l', 'control_r']:
            return '<ctrl>'
        elif key in ['shift_l', 'shift_r']:
            return '<shift>'
        elif key in ['alt_l', 'alt_r']:
            return '<alt>'
        elif key == 'grave':
            return '<grave>'
        elif len(key) == 1:
            return f'<{key}>'
        else:
            return f'<{key}>'

    def remove_hotkey(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a function.")
            return

        func = self.tree.item(selected[0])['values'][0]
        self.tree.item(selected[0], values=(func, ''))

    def on_double_click(self, event):
        item = self.tree.identify('item', event.x, event.y)
        if item:
            self.assign_hotkey(item)