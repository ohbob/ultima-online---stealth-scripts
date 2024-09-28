import json
import inspect
from pynput import keyboard
import time
import threading
import os
import importlib.util
from system_functions import SystemFunctions
from ui import HotkeyConfigUI
from utils import debug
from py_stealth import *

class HotkeyConfig:
    def __init__(self, master):
        debug("Initializing HotkeyConfig", "info")
        self.master = master
        self.hotkey_listener = None
        self.config = {}
        self.function_vars = {}
        self.functions = {}
        self.autofunctions = {}
        self.load_config()
        self.discover_functions()
        self.ui = HotkeyConfigUI(master, self)
        self.current_keys = set()
        self.last_activation_time = 0
        self.activation_cooldown = 0.3
        self.load_functions()
        self.start_hotkey_listener()
        debug("HotkeyConfig initialization complete", "info")
        SystemFunctions.hotkeys_enabled = True

    def discover_functions(self):
        debug("Starting function discovery", "info")
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Discover regular functions
        functions_path = os.path.join(base_path, 'functions')
        self.discover_modules(functions_path, self.functions)
        
        # Discover auto functions
        autofunctions_path = os.path.join(base_path, 'autofunctions')
        self.discover_modules(autofunctions_path, self.autofunctions)

    def discover_modules(self, path, target_dict):
        debug(f"Discovering modules in path: {path}", "info")
        for filename in os.listdir(path):
            if filename.endswith('.py'):
                module_name = filename[:-3]
                module_path = os.path.join(path, filename)
                debug(f"Found module: {module_name} at {module_path}", "info")
                if module_name in target_dict:
                    debug(f"Skipping duplicate module: {module_name}", "warning")
                    continue
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                target_dict[module_name] = module
                debug(f"Discovered module: {module_name}", "info")

    def load_config(self):
        debug("Loading configuration", "info")
        try:
            with open('hotkey_config.json', 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {}

    def load_functions(self):
        debug("Loading functions", "info")
        # Load system functions
        for func_name, func in inspect.getmembers(SystemFunctions, predicate=inspect.isfunction):
            if not func_name.startswith('__') and not getattr(func, '_exclude_from_gui', False):
                hotkey = self.config.get(func_name, {}).get('hotkey', '')
                self.ui.tree.insert('', 'end', values=(func_name, hotkey), tags=('system',))

        # Add toggle_all_hotkeys to the list
        hotkey = self.config.get('toggle_all_hotkeys', {}).get('hotkey', '')
        self.ui.tree.insert('', 'end', values=('toggle_all_hotkeys', hotkey), tags=('system',))

        # Load discovered functions
        for module_name, module in self.functions.items():
            hotkey = self.config.get(module_name, {}).get('hotkey', '')
            self.ui.tree.insert('', 'end', values=(module_name, hotkey))
            if hasattr(module, 'main'):
                debug(f"Loaded function: {module_name}", "info")
                self.functions[module_name] = module.main  # Store the main function directly
            else:
                debug(f"Function {module_name} has no main method", "warning")

        # Load discovered auto functions
        for module_name, module in self.autofunctions.items():
            self.ui.create_function_config(module_name, module)

        self.ui.tree.tag_configure('system', background='light gray')

    def save_config(self):
        debug("Saving configuration", "info")
        for func_name, var in self.function_vars.items():
            if func_name not in self.config:
                self.config[func_name] = {}
            self.config[func_name]['enabled'] = var.get()

        for item in self.ui.tree.get_children():
            func, hotkey = self.ui.tree.item(item)['values']
            if hotkey:
                self.config[func] = {"hotkey": hotkey}

        for func_name, func in inspect.getmembers(self.functions, predicate=inspect.isfunction):
            if hasattr(func, 'enabled') or hasattr(func, 'config'):
                if func_name not in self.config:
                    self.config[func_name] = {}
                elif isinstance(self.config[func_name], str):
                    self.config[func_name] = {"hotkey": self.config[func_name]}
                
                if hasattr(func, 'enabled'):
                    self.config[func_name]['enabled'] = func.enabled
                
                for attr_name in dir(func):
                    if not attr_name.startswith('_') and attr_name != 'enabled':
                        value = getattr(func, attr_name)
                        if isinstance(value, (int, float, str, bool)):
                            self.config[func_name][attr_name] = value

        with open('hotkey_config.json', 'w') as f:
            json.dump(self.config, f)
        debug("Configuration saved successfully!", "success")
        self.start_hotkey_listener()  # Restart the listener with new configuration

    def assign_hotkey(self, item, tree):
        debug(f"Assigning hotkey for item: {item}", "info")
        try:
            func = tree.item(item, 'values')[0]
            self.master.title(f"Press hotkey for {func}")
            self.current_hotkey = []
            self.current_item = item
            self.current_tree = tree
            self.master.bind('<KeyPress>', self.on_keypress)
            self.master.bind('<KeyRelease>', self.on_keyrelease)
        except Exception as e:
            debug(f"Error in assign_hotkey: {e}", "fail")

    def on_keypress(self, event):
        debug(f"Key pressed: {event.keysym}", "info")
        key = self.get_key_string(event)
        if key not in self.current_hotkey:
            self.current_hotkey.append(key)

    def on_keyrelease(self, event):
        debug(f"Key released: {event.keysym}", "info")
        if len(self.current_hotkey) > 0:
            hotkey = '+'.join(self.current_hotkey)
            func = self.current_tree.item(self.current_item)['values'][0]
            self.current_tree.item(self.current_item, values=(func, hotkey))
            self.master.title("Hotkey Configuration")
            self.master.unbind('<KeyPress>')
            self.master.unbind('<KeyRelease>')
            self.save_config()
            debug(f"Assigned hotkey '{hotkey}' to {func}", "success")

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

    def remove_hotkey(self, item, tree):
        debug(f"Removing hotkey for item: {item}", "info")
        func = tree.item(item, 'values')[0]
        tree.set(item, 'Hotkey', '')
        if func in self.config:
            del self.config[func]
        self.save_config()
        debug(f"Removed hotkey from {func}", "info")

    def start_hotkey_listener(self):
        debug("Starting hotkey listener", "info")
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        self.hotkey_listener = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
        self.hotkey_listener.start()
        debug("Hotkey listener started", "success")

    def on_key_press(self, key):
        debug(f"Key pressed: {key}", "info")
        current_time = time.time()
        if current_time - self.last_activation_time < self.activation_cooldown:
            debug("Ignoring rapid repeated activation", "info")
            return  # Ignore rapid repeated activations

        if isinstance(key, keyboard.Key):
            self.current_keys.add(key)
        elif isinstance(key, keyboard.KeyCode):
            self.current_keys.add(key.char.lower())
        
        debug(f"Current keys: {self.current_keys}", "info")
        self.check_hotkeys()

    def on_key_release(self, key):
        debug(f"Key released: {key}", "info")
        if isinstance(key, keyboard.Key):
            self.current_keys.discard(key)
        elif isinstance(key, keyboard.KeyCode):
            self.current_keys.discard(key.char.lower())

    def check_hotkeys(self):
        debug("Checking hotkeys", "info")
        for item in self.ui.tree.get_children():
            func, hotkey_str = self.ui.tree.item(item)['values']
            if hotkey_str:
                hotkey = self.parse_hotkey(hotkey_str)
                debug(f"Checking hotkey for {func}: {hotkey}", "info")
                if all(k in self.current_keys for k in hotkey):
                    current_time = time.time()
                    if current_time - self.last_activation_time >= self.activation_cooldown:
                        debug(f"Activating function: {func}", "info")
                        self.activate_function(func)
                        self.last_activation_time = current_time
                    else:
                        debug(f"Cooldown active for {func}", "info")
                    break
                else:
                    debug(f"Hotkey not matched for {func}", "info")

    def activate_function(self, func_name):
        debug(f"Attempting to activate function: {func_name}", "info")
        if hasattr(SystemFunctions, func_name):
            debug(f"Executing system function: {func_name}", "info")
            getattr(SystemFunctions, func_name)()
        elif func_name in self.functions:
            debug(f"Executing user function: {func_name}", "info")
            func = self.functions[func_name]
            if callable(func):
                func(self)  # Pass self as the config argument
            else:
                debug(f"Function {func_name} is not callable", "warning")
        else:
            debug(f"Function {func_name} not found", "warning")

    def parse_hotkey(self, hotkey_str):
        debug(f"Parsing hotkey string: {hotkey_str}", "info")
        keys = hotkey_str.lower().split('+')
        parsed = set()
        for key in keys:
            if key == '<ctrl>':
                parsed.add(keyboard.Key.ctrl)
            elif key == '<alt>':
                parsed.add(keyboard.Key.alt)
            elif key == '<shift>':
                parsed.add(keyboard.Key.shift)
            elif key == '<grave>':
                parsed.add('`')
            elif key.startswith('<') and key.endswith('>'):
                parsed.add(key[1:-1])
            else:
                parsed.add(key)
        return parsed

    def toggle_all_hotkeys(self):
        debug("Toggling all hotkeys", "info")
        SystemFunctions.toggle_all_hotkeys()

    def get_friends_list(self):
        debug("Getting friends list", "info")
        return self.config.get('friends', [])

    def get_pets_list(self):
        debug("Getting pets list", "info")
        return self.config.get('pets', [])