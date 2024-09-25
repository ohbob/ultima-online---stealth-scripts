from py_stealth import *
import json
import tkinter as tk
from tkinter import ttk, messagebox
from pynput import keyboard
import inspect
from pynput.keyboard import Key, KeyCode
import time
from typing import Literal


def debug(message: str, color: Literal["success", "fail", "info", "warning"] = "info") -> None:
    color_map = {
        "success": 60,  # Green
        "fail": 30,     # Red
        "info": 5,      # Blue
        "warning": 40   # Orange
    }
    ClientPrintEx(Self(), color_map[color], 1, f"* {message.upper()} *")

def configurable_function(**kwargs):
    def decorator(func):
        func.config = kwargs
        return func
    return decorator

def exclude_from_gui(func):
    func._exclude_from_gui = True
    return func
# ------------------------------------------------------------------------------------

def main_loop():
    while True:
        if SystemFunctions.hotkeys_enabled:
            if Functions.autoheal_enabled:
                if GetHP(Self()) < MaxHP():
                    Functions.heal_self()
        time.sleep(0.1)  # Small delay to prevent excessive CPU usage

class Functions:
    autoheal_enabled = False
    autoheal_threshold = 95  # Default value, can be changed via config

    @configurable_function(enabled=True, threshold=95)
    def heal_self():
        debug("Healing Self", "success")
        # Add actual healing logic here

    def hide():
        if not Hidden():
            UseSkill('Hiding')
            debug("Not hidden", "warning")
        else:
            debug("Already hidden", "info")

    def cast_magic_arrow():
        debug("Casting Magic Arrow", "info")

    def cancel_target():
        if TargetPresent():
            CancelTarget()
            debug("Target Canceled", "warning")


    def toggle_autoheal():
        Functions.autoheal_enabled = not Functions.autoheal_enabled
        debug(f"Autoheal {'enabled' if Functions.autoheal_enabled else 'disabled'}", 
              "success" if Functions.autoheal_enabled else "fail")

    @exclude_from_gui
    def secret_function():
        # This function won't appear in the GUI
        pass

# ------------------------------------------------------------------------------------



class SystemFunctions:
    hotkeys_enabled = True

    @staticmethod
    def toggle_all_hotkeys():
        SystemFunctions.hotkeys_enabled = not SystemFunctions.hotkeys_enabled
        debug(f"Hotkeys {'enabled' if SystemFunctions.hotkeys_enabled else 'disabled'}", 
              "success" if SystemFunctions.hotkeys_enabled else "fail")

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

        self.load_functions()
        self.load_config()

    def load_functions(self):
        for func_name, func in inspect.getmembers(SystemFunctions, predicate=inspect.isfunction):
            if not func_name.startswith('__') and not getattr(func, '_exclude_from_gui', False):
                self.tree.insert('', 'end', values=(func_name, ''), tags=('system',))
        
        for func_name, func in inspect.getmembers(Functions, predicate=inspect.isfunction):
            if not func_name.startswith('__') and func_name != 'main_loop' and not getattr(func, '_exclude_from_gui', False):
                self.tree.insert('', 'end', values=(func_name, ''))
                if hasattr(func, 'config'):
                    self.create_function_config(func_name, func.config)

        self.tree.tag_configure('system', background='light gray')

    def create_function_config(self, func_name, config):
        frame = ttk.LabelFrame(self.config_frame, text=func_name)
        frame.pack(pady=5, padx=10, fill=tk.X)

        for param, default in config.items():
            if isinstance(default, bool):
                var = tk.BooleanVar(value=default)
                ttk.Checkbutton(frame, text=param, variable=var).pack(anchor=tk.W)
            elif isinstance(default, (int, float)):
                var = tk.DoubleVar(value=default)
                ttk.Label(frame, text=f"{param}:").pack(side=tk.LEFT)
                ttk.Entry(frame, textvariable=var, width=10).pack(side=tk.LEFT, padx=5)
            else:
                var = tk.StringVar(value=str(default))
                ttk.Label(frame, text=f"{param}:").pack(side=tk.LEFT)
                ttk.Entry(frame, textvariable=var).pack(side=tk.LEFT, padx=5)

            setattr(self, f"{func_name}_{param}", var)

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
                    if hasattr(Functions, func):
                        func_obj = getattr(Functions, func)
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

        for func_name, func in inspect.getmembers(Functions, predicate=inspect.isfunction):
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
        # print(f"Key pressed: {key}")  # Debug: Print the pressed key

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
            return f'<{key}>'  # Wrap single characters (including numbers) in angle brackets
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

if __name__ == "__main__":
    root = tk.Tk()
    app = HotkeyConfig(root)
    root.mainloop()

    # After GUI closes, set up global hotkeys
    try:
        with open('hotkey_config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("No hotkey configuration found. Please set up hotkeys and save.")
        exit()

    def on_activate(func_name, func_config):
        if SystemFunctions.hotkeys_enabled or func_name == 'toggle_all_hotkeys':
            if hasattr(SystemFunctions, func_name):
                getattr(SystemFunctions, func_name)()
            elif hasattr(Functions, func_name):
                func = getattr(Functions, func_name)
                if func_name == 'toggle_autoheal':
                    Functions.toggle_autoheal()
                else:
                    if func_config:
                        for key, value in func_config.items():
                            setattr(Functions, f"{func_name}_{key}", value)
                    if 'enabled' in func_config:
                        current_state = getattr(Functions, f"{func_name}_enabled", True)
                        setattr(Functions, f"{func_name}_enabled", not current_state)
                    func()
        else:
            debug(f"Hotkey for {func_name} pressed, but hotkeys are disabled", "fail")

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

    hotkeys = {}
    for func, data in config.items():
        if isinstance(data, dict):
            hotkey_str = data['hotkey']
            func_config = {k: v for k, v in data.items() if k != 'hotkey'}
        else:
            hotkey_str = data
            func_config = {}
        
        hotkey = parse_hotkey(hotkey_str)
        hotkeys[hotkey] = (func, func_config)

    print("Registered hotkeys:", ['+'.join(str(k) for k in combo) for combo in hotkeys.keys()])

    current_keys = set()

    def on_press(key):
        if isinstance(key, Key):
            current_keys.add(key)
        elif isinstance(key, KeyCode):
            current_keys.add(key)
        
        # Check for custom hotkeys
        for hotkey, (func, func_config) in hotkeys.items():
            if all(k in current_keys for k in hotkey):
                on_activate(func, func_config)
                return

    def on_release(key):
        current_keys.discard(key)

    import threading
    main_thread = threading.Thread(target=main_loop, daemon=True)
    main_thread.start()

    # Use a regular Listener instead of GlobalHotKeys:
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    print("Hotkeys activated. Press keys to test. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        listener.stop()