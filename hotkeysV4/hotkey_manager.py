import tkinter as tk
from tkinter import ttk, messagebox
from pynput import keyboard
import json
import time
import os
import importlib.util
import sys
import threading
from py_stealth import *

# Add the parent directory to sys.path to allow imports from sibling directories
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Use absolute imports for the tab modules
from hotkeysV4.core.scripts_tab import ScriptsTab
from hotkeysV4.core.auto_functions_tab import AutoFunctionsTab
from hotkeysV4.core.friends_tab import FriendsTab
from hotkeysV4.core.pets_tab import PetsTab

# Move the standalone debug function outside the class
def debug(message: str, level: str = "info", client=False) -> None:
    color_map = {
        "success": 60,  # Green
        "fail": 30,     # Red
        "info": 10,      # Blue
        "warning": 40   # Orange
    }
    if client:
        ClientPrintEx(Self(), color_map[level], 1, f"* {message.upper()} *")
    print(message)

class HotkeyManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Hotkey Manager v4")
        self.hotkeys = {}
        self.auto_functions = {}
        self.friends = []
        self.pets = []
        self.current_keys = set()
        self.last_activation_time = 0
        self.activation_cooldown = 0.3
        self.functions = {}
        self.autofunctions = {}
        self.hotkeys_enabled = True
        self.auto_functions_enabled = False
        self.hotkey_listener = None
        self.system_functions = {}
        self.discovered_functions = {}
        self.flattened_functions = {}
        self.discover_all_functions()
        self.create_widgets()
        self.load_config()
        self.start_hotkey_listener()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.scripts_tab = ScriptsTab(self.notebook, self)
        self.auto_functions_tab = AutoFunctionsTab(self.notebook, self)
        self.friends_tab = FriendsTab(self.notebook, self)
        self.pets_tab = PetsTab(self.notebook, self)

        # Set the auto_functions_tab attribute
        self.auto_functions_tab = self.auto_functions_tab

    def load_config(self):
        try:
            with open('hotkey_config.json', 'r') as f:
                config = json.load(f)
                self.hotkeys = config.get('hotkeys', {})
                self.auto_functions = config.get('auto_functions', {})
                self.auto_function_order = config.get('auto_function_order', [])
                self.friends = config.get('friends', [])
                self.pets = config.get('pets', [])
                self.activation_cooldown = config.get('activation_cooldown', 0.3)

            self.discover_functions()
            self.populate_tree_views()

        except FileNotFoundError:
            debug("Config file not found. Starting with empty configuration.", "warning")

    def discover_functions(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        functions_path = os.path.join(base_path, 'functions')
        self.discover_modules(functions_path, self.functions, is_auto=False)
        
        autofunctions_path = os.path.join(base_path, 'autofunctions')
        self.discover_modules(autofunctions_path, self.autofunctions, is_auto=True)

    def discover_modules(self, path, target_dict, is_auto):
        if not os.path.exists(path):
            debug(f"Path does not exist: {path}", "warning")
            return

        for filename in os.listdir(path):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                module_path = os.path.join(path, filename)
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                
                # Add py_stealth functions to the module's global namespace
                module.__dict__.update({name: func for name, func in globals().items() if callable(func) and not name.startswith('__')})
                
                try:
                    spec.loader.exec_module(module)
                except Exception as e:
                    debug(f"Error loading module {module_name}: {str(e)}", "fail")
                    continue
                
                if hasattr(module, 'main'):
                    target_dict[module_name] = module.main
                    debug(f"Discovered {'auto ' if is_auto else ''}function: {module_name}", "info")
                    
                    if is_auto:
                        # Initialize auto function in self.auto_functions
                        self.auto_functions[module_name] = {
                            'enabled': False,
                            'variable1': '',
                            'variable2': '',
                            'variable3': '',
                            'hotkey': ''
                        }

    def discover_all_functions(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        autodiscovery_path = os.path.join(base_path, 'autodiscovery')
        for root, dirs, files in os.walk(autodiscovery_path):
            dirs[:] = [d for d in dirs if d != '__pycache__']
            
            relative_path = os.path.relpath(root, autodiscovery_path)
            if relative_path == '.':
                continue
            category = relative_path.replace(os.path.sep, '_')
            self.discovered_functions[category] = {}
            self.discover_modules(root, self.discovered_functions[category], is_auto=False)
    
        # Flatten the discovered functions for easier access
        self.flattened_functions = {}
        for category, functions in self.discovered_functions.items():
            for func_name, func in functions.items():
                self.flattened_functions[f"{category}_{func_name}"] = func
    
        debug(f"Discovered functions: {list(self.flattened_functions.keys())}", "info")

    def populate_tree_views(self):
        all_hotkeys = self.hotkeys.copy()
        for category, functions in self.discovered_functions.items():
            all_hotkeys.update({f"{func}": self.hotkeys.get(f"{func}", '') for func in functions})
        
        system_functions = self.discovered_functions.get('system_functions', {})
        regular_functions = {k: v for k, v in self.discovered_functions.items() if k != 'system_functions'}
        
        self.scripts_tab.load_hotkeys(all_hotkeys, system_functions, regular_functions)

        self.auto_functions_tab.tree.delete(*self.auto_functions_tab.tree.get_children())  # Clear existing items
        for func_name in self.auto_function_order:
            if func_name in self.auto_functions:
                auto_func_data = self.auto_functions[func_name]
                enabled = auto_func_data.get('enabled', False)
                var1 = auto_func_data.get('variable1', '')
                var2 = auto_func_data.get('variable2', '')
                var3 = auto_func_data.get('variable3', '')
                hotkey = auto_func_data.get('hotkey', '')
                tag = 'enabled' if enabled else 'disabled'
                self.auto_functions_tab.tree.insert('', 'end', values=(func_name, var1, var2, var3, hotkey, 'True' if enabled else 'False'), tags=(tag,))

        # Add any new functions that are not in the order
        for func_name in self.auto_functions:
            if func_name not in self.auto_function_order:
                auto_func_data = self.auto_functions[func_name]
                enabled = auto_func_data.get('enabled', False)
                var1 = auto_func_data.get('variable1', '')
                var2 = auto_func_data.get('variable2', '')
                var3 = auto_func_data.get('variable3', '')
                hotkey = auto_func_data.get('hotkey', '')
                tag = 'enabled' if enabled else 'disabled'
                self.auto_functions_tab.tree.insert('', 'end', values=(func_name, var1, var2, var3, hotkey, 'True' if enabled else 'False'), tags=(tag,))
                self.auto_function_order.append(func_name)

        self.friends_tab.load_friends(self.friends)
        self.pets_tab.load_pets(self.pets)

        # Create a hierarchical tree view structure
        self.scripts_tab.tree.delete(*self.scripts_tab.tree.get_children())  # Clear existing items
        for category, functions in self.discovered_functions.items():
            if functions:  # Only add non-empty categories
                category_id = self.scripts_tab.tree.insert('', 'end', text=category)
                for func_name in functions:
                    hotkey = self.hotkeys.get(func_name, '')
                    display_text = f"{func_name} ({hotkey})" if hotkey else func_name
                    self.scripts_tab.tree.insert(category_id, 'end', text=display_text)

        self.auto_functions_tab.update_toggle_button()

    def save_config(self):
        config = {
            'hotkeys': self.hotkeys,
            'auto_functions': self.auto_functions,
            'auto_function_order': self.auto_function_order,
            'friends': self.friends,
            'pets': self.pets,
            'activation_cooldown': self.activation_cooldown
        }
        with open('hotkey_config.json', 'w') as f:
            json.dump(config, f)

    def start_hotkey_listener(self):
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        self.hotkey_listener = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
        self.hotkey_listener.start()

    def on_key_press(self, key):
        try:
            if isinstance(key, keyboard.Key):
                self.current_keys.add(key)
            elif isinstance(key, keyboard.KeyCode):
                if key.char == '`':
                    self.current_keys.add('`')
                else:
                    self.current_keys.add(key.char.lower())
        except AttributeError:
            pass
        self.check_hotkeys()

    def on_key_release(self, key):
        try:
            if isinstance(key, keyboard.Key):
                self.current_keys.discard(key)
            elif isinstance(key, keyboard.KeyCode):
                if key.char == '`':
                    self.current_keys.discard('`')
                else:
                    self.current_keys.discard(key.char.lower())
        except AttributeError:
            pass

    def check_hotkeys(self):
        current_time = time.time()
        if current_time - self.last_activation_time < self.activation_cooldown:
            return

        current_hotkey = set()
        for key in self.current_keys:
            if isinstance(key, keyboard.Key):
                if key == keyboard.Key.ctrl:
                    current_hotkey.add('ctrl')
                elif key == keyboard.Key.alt:
                    current_hotkey.add('alt')
                elif key == keyboard.Key.shift:
                    current_hotkey.add('shift')
                else:
                    current_hotkey.add(key.name)
            else:
                current_hotkey.add(key)

        for func, hotkey in self.hotkeys.items():
            hotkey_set = set(hotkey.lower().replace('<', '').replace('>', '').split('+'))
            if hotkey_set == current_hotkey:
                # debug(f"Hotkey match found for function: {func}", "info", False)
                self.activate_function(func)
                self.last_activation_time = current_time
                break

    def activate_function(self, func_name):
        # debug(f"Attempting to activate function: {func_name}", "info")
        if func_name in ['toggle_all_hotkeys', 'toggle_auto_functions']:
            if func_name == 'toggle_all_hotkeys':
                self.toggle_all_hotkeys()
            else:
                self.toggle_all_auto_functions()
        elif not self.hotkeys_enabled:
            debug("Hotkeys are currently disabled", "warning")
        else:
            for category, functions in self.discovered_functions.items():
                if func_name in functions:
                    # debug(f"Calling discovered function: {func_name}", "info")
                    try:
                        func = functions[func_name]
                        if 'config' in func.__code__.co_varnames or 'manager' in func.__code__.co_varnames:
                            func(self)
                        else:
                            func()
                    except Exception as e:
                        debug(f"Error calling discovered function {func_name}: {str(e)}", "fail")
                    return
            if func_name in self.autofunctions:
                if self.auto_functions_enabled:
                    debug(f"Toggling auto function: {func_name}", "info")
                    self.toggle_auto_function(func_name)
                else:
                    debug("Auto functions are currently disabled", "warning")
            else:
                debug(f"Function {func_name} not found", "warning")

    def toggle_all_hotkeys(self):
        self.hotkeys_enabled = not self.hotkeys_enabled
        status = "enabled" if self.hotkeys_enabled else "disabled"
        debug(f"All hotkeys are now {status}", "info")

    def toggle_all_auto_functions(self):
        self.auto_functions_enabled = not self.auto_functions_enabled
        status = "enabled" if self.auto_functions_enabled else "disabled"
        self.debug(f"All auto functions are now {status}", "info")
        
        # Update the button state in the AutoFunctionsTab
        if hasattr(self, 'auto_functions_tab'):
            self.auto_functions_tab.update_toggle_button()
        
        return self.auto_functions_enabled

    def assign_hotkey(self, item, tree):
        func = tree.item(item, 'values')[0]  # Get function name from the first column
        self.master.title(f"Press new hotkey for {func}")
        self.current_hotkey = set()
        self.current_item = item
        self.current_tree = tree
        self.listening_for_hotkey = True
        self.master.bind('<KeyPress>', self.on_hotkey_press)
        self.master.bind('<KeyRelease>', self.on_hotkey_release)

    def on_hotkey_press(self, event):
        if self.listening_for_hotkey:
            key = self.get_key_string(event)
            self.current_hotkey.add(key)

    def on_hotkey_release(self, event):
        if self.listening_for_hotkey:
            self.listening_for_hotkey = False
            hotkey = '+'.join(sorted(self.current_hotkey))
            func = self.current_tree.item(self.current_item, 'values')[0]
            if self.current_tree == self.auto_functions_tab.tree:
                values = list(self.current_tree.item(self.current_item, 'values'))
                values[4] = hotkey  # Update hotkey in the 5th column
                self.current_tree.item(self.current_item, values=values)
                self.auto_functions[func]['hotkey'] = hotkey
            else:
                self.hotkeys[func] = hotkey
            self.master.title("Hotkey Manager")
            self.master.unbind('<KeyPress>')
            self.master.unbind('<KeyRelease>')
            self.save_config()
            debug(f"Assigned hotkey '{hotkey}' to {func}", "success")

    def get_key_string(self, event):
        key = event.keysym.lower()
        if key in ['control_l', 'control_r']:
            return 'ctrl'
        elif key in ['alt_l', 'alt_r']:
            return 'alt'
        elif key in ['shift_l', 'shift_r']:
            return 'shift'
        elif key == 'grave' or key == '`':
            return '`'
        else:
            return key

    def run(self):
        # Start the auto functions loop in a separate thread
        auto_functions_thread = threading.Thread(target=self.run_auto_functions, daemon=True)
        auto_functions_thread.start()

        self.master.mainloop()

    def toggle_auto_function(self, func_name):
        if func_name in self.auto_functions:
            self.auto_functions[func_name]['enabled'] = not self.auto_functions[func_name].get('enabled', False)
            enabled = self.auto_functions[func_name]['enabled']
            self.auto_functions_tab.update_enabled_status(func_name, enabled)
            
            if enabled and not self.auto_functions_enabled:
                self.debug(f"Auto function {func_name} enabled, but auto functions are globally disabled", "warning")
            elif enabled:
                self.debug(f"Auto function {func_name} enabled and will run when conditions are met", "info")
            else:
                self.debug(f"Auto function {func_name} disabled", "info")
            
            self.save_config()

    def start_auto_function(self, func_name):
        if func_name in self.auto_functions:
            auto_func_data = self.auto_functions[func_name]
            threshold = auto_func_data.get('threshold', 0)
            func = self.autofunctions.get(func_name)
            if func:
                thread = threading.Thread(target=self.run_auto_function, args=(func_name, func, threshold), daemon=True)
                thread.start()

    def stop_auto_function(self, func_name):
        if func_name in self.auto_functions:
            auto_func_data = self.auto_functions[func_name]
            if 'thread' in auto_func_data:
                thread = auto_func_data['thread']
                if thread.is_alive():
                    thread.join()
                del auto_func_data['thread']

    def run_auto_function(self, func_name, func, threshold):
        while self.auto_functions[func_name].get('enabled', False):
            try:
                result = func(self)
                if result >= threshold:
                    debug(f"Auto function {func_name} triggered with result: {result}", "info")
                    # Add any additional actions here
            except Exception as e:
                debug(f"Error running auto function {func_name}: {str(e)}", "fail")
            time.sleep(1)  # Adjust the sleep duration as needed

    def get_pets_list(self):
        return self.pets

    def get_friends_list(self):
        return self.friends

    def update_friends_list(self, new_friends):
        self.friends = new_friends
        self.save_config()

    def update_pets_list(self, new_pets):
        self.pets = new_pets
        self.save_config()

    def GetName(self, object_id):
        return GetName(object_id)

    def launch_selected_function(self):
        selected = self.scripts_tab.tree.selection()
        if selected:
            func_name = self.scripts_tab.tree.item(selected[0], 'text').split(' (')[0]
            self.activate_function(func_name)
        else:
            debug("No function selected", "warning")

    def getTargetID(self) -> int:
        ClientRequestObjectTarget()
        WaitForClientTargetResponse(60000)
        if ClientTargetResponsePresent():
            response = ClientTargetResponse()
            if isinstance(response, dict):
                item_id = response.get('ID', None)
                return item_id
        return None

    def debug(self, message: str, level: str = "info", client=False) -> None:
        color_map = {
            "success": 60,  # Green
            "fail": 30,     # Red
            "info": 10,      # Blue
            "warning": 40   # Orange
        }
        if client:
            ClientPrintEx(Self(), color_map[level], 1, f"* {message.upper()} *")
        print(message)

    def remove_hotkey(self, item, tree):
        func = tree.item(item, 'text').split(' (')[0]
        if func in self.hotkeys:
            del self.hotkeys[func]
            tree.item(item, text=func)  # Remove the hotkey from the display
            self.save_config()
            debug(f"Removed hotkey for {func}", "success")
        else:
            debug(f"No hotkey assigned to {func}", "warning")

    def update_auto_function_order(self, new_order):
        self.auto_function_order = new_order
        self.save_config()

    def run_auto_functions(self):
        while True:
            if self.auto_functions_enabled:
                for func_name in self.auto_function_order:
                    if func_name in self.auto_functions and self.auto_functions[func_name].get('enabled', False):
                        func = self.autofunctions.get(func_name)
                        if func:
                            try:
                                var1 = self.auto_functions[func_name].get('variable1', '')
                                var2 = self.auto_functions[func_name].get('variable2', '')
                                var3 = self.auto_functions[func_name].get('variable3', '')
                                self.debug(f"Executing {func_name} with variables: {var1}, {var2}, {var3}", "info")
                                result = func(self, var1, var2, var3)
                                if result:
                                    self.debug(f"Auto function {func_name} executed with result: {result}", "info")
                            except Exception as e:
                                self.debug(f"Error in auto function {func_name}: {str(e)}", "fail")
            time.sleep(self.activation_cooldown)

    def update_auto_function_variable(self, func_name, var_index, value):
        if func_name in self.auto_functions:
            self.auto_functions[func_name][f'variable{var_index}'] = value
            self.save_config()

def main():
    root = tk.Tk()
    app = HotkeyManager(root)
    
    app.run()

if __name__ == "__main__":
    main()