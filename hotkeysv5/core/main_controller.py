from controllers.auto_discovery_controller import AutoDiscoveryController
from controllers.hotkeys_controller import HotkeysController
from controllers.friends_controller import FriendsController
from controllers.pets_controller import PetsController
from controllers.scripts_controller import ScriptsController
from controllers.auto_functions_controller import AutoFunctionsController
from core.state import State
import importlib
import sys
import io
import time
from contextlib import redirect_stdout
from core.py_stealth import *
from core.uo_globals import *  # Import the global functions
from socket import error as SocketError
from errno import ECONNREFUSED
import threading
import json
from core.hotkey_controller import HotkeyController

class MainController:
    def __init__(self, py_stealth):
        self.py_stealth = py_stealth
        self.state = State()
        self.hotkeys_controller = HotkeysController(self.state)
        self.friends_controller = FriendsController(self.state, self.py_stealth)
        self.pets_controller = PetsController(self.state, self.py_stealth)
        self.scripts_controller = ScriptsController(self.state, self)
        self.auto_functions_controller = AutoFunctionsController(self.state)
        self.auto_discovery_controller = AutoDiscoveryController(self.state)
        self.ui = None
        self.scripts_tab = None  # This will be set when creating the UI
        self.hotkeys_enabled = False  # Initial state
        self.auto_functions = {}  # Initialize auto_functions as an empty dictionary
        self.load_auto_functions()  # Load saved auto functions
        self.discover_all_functions()
        self.hotkey_controller = HotkeyController(self)
        self.hotkeys = {}

        if not self.initialize_stealth_connection():
            raise ConnectionError("Failed to initialize Stealth connection")

        self.main_thread = threading.Thread(target=self.main_loop)
        self.main_thread.daemon = True
        self.main_thread.start()

        self.config_file = 'config.json'
        self.load_config()  # Load configuration at startup

    def set_ui(self, ui):
        self.ui = ui
        if hasattr(ui, 'scripts_tab'):
            self.scripts_tab = ui.scripts_tab
        loaded_hotkeys = self.load_config()  # Load config and get hotkeys
        self.update_ui_after_config_load()  # Update UI with loaded config
        self.update_ui_with_discovered_functions()  # Update UI after it's set
        if self.scripts_tab:
            self.scripts_tab.populate_tree()  # This will now populate the tree with hotkeys
            hotkeys = self.hotkey_controller.get_hotkeys()
            print("Setting UI with hotkeys:", hotkeys)
            self.scripts_tab.update_hotkeys_display(hotkeys)  # Ensure hotkeys are displayed

    def set_hotkey(self, hotkey, func_name):
        self.hotkey_controller.setup_hotkey(hotkey, func_name)
        self.save_config()
        if self.scripts_tab:
            self.scripts_tab.update_hotkeys_display(self.hotkey_controller.get_hotkeys())
        self.print_current_state()

    def clear_hotkey(self, hotkey):
        self.hotkey_controller.clear_hotkey(hotkey)
        self.save_config()
        self.print_current_state()

    def run_once(self, func_name):
        print(f"Running function once: {func_name}")
        if hasattr(self, 'scripts_controller'):
            self.scripts_controller.run_script(func_name, loop=False)
        else:
            print(f"Warning: Unable to run {func_name}. scripts_controller not found.")

    def handle_key_press(self, event):
        hotkey = self.get_hotkey_from_event(event)
        if hotkey and hotkey in self.hotkeys:
            func_name = self.hotkeys[hotkey]
            self.run_once(func_name)

    def get_hotkey_from_event(self, event):
        modifiers = []
        if event.state & 0x4:
            modifiers.append('Ctrl')
        if event.state & 0x1:
            modifiers.append('Shift')
        if event.state & 0x8:
            modifiers.append('Alt')
        
        key = event.keysym
        if key in ['Control_L', 'Control_R', 'Shift_L', 'Shift_R', 'Alt_L', 'Alt_R']:
            return None  # Ignore modifier key presses on their own
        
        return '+'.join(modifiers + [key])

    def set_scripts_timeout(self, timeout):
        try:
            timeout = int(timeout)
            self.state.set_scripts_timeout(timeout)
            print(f"Scripts timeout set to: {timeout} ms")
            self.save_config()
            self.print_current_state()
        except ValueError:
            print("Invalid timeout value. Please enter a valid integer.")

    def set_auto_functions_timeout(self, timeout):
        try:
            timeout = int(timeout)
            self.state.set_auto_functions_timeout(timeout)
            print(f"Auto functions timeout set to: {timeout} ms")
            self.save_config()
            self.print_current_state()
        except ValueError:
            print("Invalid timeout value. Please enter a valid integer.")

    def toggle_all_auto_functions(self):
        new_state = not self.state.auto_functions_enabled
        self.state.set_auto_functions_enabled(new_state)
        self.auto_functions_controller.set_all_auto_functions_state(new_state)
        print(f"Auto functions {'enabled' if new_state else 'disabled'}")
        self.save_config()
        self.print_current_state()
        if self.ui and hasattr(self.ui, 'auto_functions_tab'):
            self.ui.auto_functions_tab.update_auto_button_state(new_state)
        return new_state

    def toggle_all_hotkeys(self):
        new_state = self.hotkey_controller.toggle_all_hotkeys()
        self.state.set_hotkeys_enabled(new_state)
        
        print(f"Hotkeys {'enabled' if new_state else 'disabled'}")
        
        # Update UI
        if self.ui and hasattr(self.ui, 'scripts_tab'):
            self.ui.scripts_tab.update_hotkey_button_state(new_state)
        
        self.save_config()
        return new_state

    def save_config(self):
        config = {
            'hotkeys_enabled': self.state.hotkeys_enabled,
            'loop_enabled': self.state.loop_enabled,
            'auto_functions_enabled': self.state.auto_functions_enabled,
            'scripts_timeout': self.state.scripts_timeout,
            'auto_functions_timeout': self.state.auto_functions_timeout,
            'hotkeys': self.hotkey_controller.get_hotkeys(),
            'friends': self.state.friends,
            'pets': self.state.pets,
            'auto_functions': self._serialize_auto_functions()
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print("Configuration saved successfully")

    def _serialize_auto_functions(self):
        serialized = {}
        for category, functions in self.state.auto_functions.items():
            serialized[category] = {}
            for func_name, func_data in functions.items():
                serialized[category][func_name] = {
                    'enabled': func_data.get('enabled', False),
                    'path': func_data.get('path', ''),
                    'hotkey': func_data.get('hotkey', '')
                }
        return serialized

    def load_config(self):
        try:
            print("Hotkeys before loading config:", self.hotkey_controller.get_hotkeys())
            
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            self.state.set_hotkeys_enabled(config.get('hotkeys_enabled', False))
            self.state.set_loop_enabled(config.get('loop_enabled', False))
            self.state.set_auto_functions_enabled(config.get('auto_functions_enabled', False))
            self.state.set_scripts_timeout(config.get('scripts_timeout', 5000))
            self.state.set_auto_functions_timeout(config.get('auto_functions_timeout', 5000))
            
            loaded_hotkeys = config.get('hotkeys', {})
            self.hotkey_controller.set_hotkeys(loaded_hotkeys)
            
            self.state.friends = config.get('friends', [])
            self.state.pets = config.get('pets', [])
            
            loaded_auto_functions = config.get('auto_functions', {})
            
            for category, functions in loaded_auto_functions.items():
                if category not in self.state.auto_functions:
                    self.state.auto_functions[category] = {}
                for func_name, func_data in functions.items():
                    if func_name in self.state.auto_functions[category]:
                        self.state.auto_functions[category][func_name].update(func_data)
                    else:
                        self.state.auto_functions[category][func_name] = func_data
            
            self.friends_controller.set_friends(self.state.friends)
            self.pets_controller.set_pets(self.state.pets)
            
            if self.ui:
                self.update_ui_after_config_load()
            
            print("Configuration loaded successfully")
            print("Hotkeys after loading config:", self.hotkey_controller.get_hotkeys())
            return loaded_hotkeys  # Return the loaded hotkeys
        except FileNotFoundError:
            print("No configuration file found. Starting with default settings.")
        except json.JSONDecodeError:
            print("Error decoding configuration file. Starting with default settings.")
        return {}  # Return an empty dict if loading fails

    def update_ui_after_config_load(self):
        if hasattr(self.ui, 'friends_tab'):
            self.ui.friends_tab.populate_tree()
        if hasattr(self.ui, 'pets_tab'):
            self.ui.pets_tab.populate_tree()
        if hasattr(self.ui, 'scripts_tab'):
            self.ui.scripts_tab.populate_tree()
            hotkeys = self.hotkey_controller.get_hotkeys()
            print("Updating UI with hotkeys:", hotkeys)
            self.ui.scripts_tab.update_hotkeys_display(hotkeys)
        if hasattr(self.ui, 'auto_functions_tab'):
            self.ui.auto_functions_tab.populate_tree()

    def discover_all_functions(self):
        print("Starting function discovery...")
        self.auto_discovery_controller.discover_all_functions()
        self.state.print_discovered_functions()
        print("Function discovery complete")

    def update_ui_with_discovered_functions(self):
        if self.ui:
            print("Updating UI with discovered functions...")
            self.ui.scripts_tab.populate_tree()
            self.ui.auto_functions_tab.populate_tree()
        else:
            print("UI not set, skipping UI update")

    def set_hotkeys_state(self, state):
        self.state.set_hotkeys_enabled(state)
        if state:
            self.hotkey_controller.start()
        else:
            self.hotkey_controller.stop()
        print(f"Hotkeys {'enabled' if state else 'disabled'}")
        self.save_config()
        self.print_current_state()

    def set_loop_state(self, enabled):
        self.state.set_loop_enabled(enabled)
        print(f"Loop {'enabled' if enabled else 'disabled'}")
        self.print_current_state()

    def set_auto_functions_state(self, enabled):
        print(f"Attempting to {'enable' if enabled else 'disable'} auto functions...")
        self.state.set_auto_functions_enabled(enabled)
        print(f"Auto functions {'enabled' if enabled else 'disabled'}")
        
        if self.ui and hasattr(self.ui, 'auto_functions_tab'):
            self.ui.auto_functions_tab.update_auto_button_state(enabled)
        
        self.print_current_state()

    def print_current_state(self):
        print("\nCurrent Application State:")
        print(f"Hotkeys Enabled: {self.state.hotkeys_enabled}")
        print(f"Loop Enabled: {self.state.loop_enabled}")
        print(f"Auto Functions Enabled: {self.state.auto_functions_enabled}")
        print(f"Scripts Timeout: {self.state.scripts_timeout} ms")
        print(f"Auto Functions Timeout: {self.state.auto_functions_timeout} ms")
        print(f"Number of Hotkeys: {len(self.state.hotkeys)}")
        print(f"Number of Friends: {len(self.state.friends)}")
        print(f"Number of Pets: {len(self.state.pets)}")
        print(f"Number of Discovered Functions: {sum(len(funcs) for funcs in self.state.discovered_functions.values())}")
        print(f"Number of Auto Functions: {sum(len(funcs) for funcs in self.state.auto_functions.values())}")
        print()  # Empty line for better readability

    def get_discovered_functions(self):
        return self.state.discovered_functions

    def get_auto_functions(self):
        return self.state.auto_functions

    def run_script(self, func_name, loop=False, timeout=None):
        print(f"Running script: {func_name}")
        print(f"Loop: {'Enabled' if loop else 'Disabled'}")
        print(f"Timeout: {timeout if timeout is not None else 'Default'} ms")

        script_path = None
        func_data = None
        for category, functions in self.state.discovered_functions.items():
            if func_name in functions:
                func_data = functions[func_name]
                script_path = func_data.get('path')
                break

        if script_path and func_data:
            self._execute_script(script_path, func_data, func_name, loop, timeout)
        else:
            print(f"Script file for {func_name} not found.")

    def run_auto_function(self, func_name, loop=False, timeout=None):
        print(f"Running auto function: {func_name}")
        print(f"Loop: {'Enabled' if loop else 'Disabled'}")
        print(f"Timeout: {timeout if timeout is not None else 'Default'} ms")

        script_path = None
        func_data = None
        for category, functions in self.state.auto_functions.items():
            if func_name in functions:
                func_data = functions[func_name]
                script_path = func_data.get('path')
                break

        if script_path and func_data:
            self._execute_auto_function(script_path, func_data, func_name, loop, timeout)
        else:
            print(f"Auto function script for {func_name} not found.")

    def _execute_script(self, script_path, func_data, func_name, loop, timeout):
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            try:
                script_namespace = self._prepare_script_namespace()
                
                with open(script_path, 'r') as script_file:
                    script_code = script_file.read()
                    exec(script_code, script_namespace)

                if 'main' in script_namespace:
                    main_func = script_namespace['main']
                    if loop:
                        start_time = time.time()
                        while True:
                            if 'main_controller' in main_func.__code__.co_varnames:
                                main_func(self)
                            else:
                                main_func()
                            if timeout and (time.time() - start_time) * 1000 >= timeout:
                                break
                    else:
                        if 'main_controller' in main_func.__code__.co_varnames:
                            main_func(self)
                        else:
                            main_func()
                else:
                    print(f"Error: 'main' function not found in {func_name}")
            except Exception as e:
                print(f"Error executing {func_name}: {str(e)}")
                import traceback
                traceback.print_exc()

        print(captured_output.getvalue())

    def _execute_auto_function(self, script_path, func_data, func_name, loop, timeout):
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            try:
                if not self.check_stealth_connection():
                    if not self.reconnect_to_stealth():
                        print(f"Cannot execute {func_name}: No connection to Stealth.")
                        return

                script_namespace = self._prepare_script_namespace()
                
                with open(script_path, 'r') as script_file:
                    script_code = script_file.read()
                    exec(script_code, script_namespace)

                if 'main' in script_namespace:
                    main_func = script_namespace['main']
                    if loop:
                        start_time = time.time()
                        while True:
                            try:
                                main_func()
                            except SocketError as e:
                                if e.errno == ECONNREFUSED:
                                    print("Lost connection to Stealth. Attempting to reconnect...")
                                    if not self.reconnect_to_stealth():
                                        break
                                else:
                                    print(f"An unexpected error occurred: {str(e)}")
                                    break
                            if timeout and (time.time() - start_time) * 1000 >= timeout:
                                break
                    else:
                        main_func()
                else:
                    print(f"Error: 'main' function not found in {func_name}")
            except Exception as e:
                print(f"Error executing {func_name}: {str(e)}")
                import traceback
                traceback.print_exc()

        print(captured_output.getvalue())

    def toggle_auto_function(self, func_name, enabled):
        for category, functions in self.state.auto_functions.items():
            if func_name in functions:
                functions[func_name]['enabled'] = enabled
                print(f"{'Enabled' if enabled else 'Disabled'} auto function: {func_name}")
                self.save_config()
                return
        print(f"Auto function '{func_name}' not found")

    def add_friend(self):
        self.friends_controller.add_friend()
        self.ui.friends_tab.populate_tree()
        self.save_config()

    def remove_friend(self, id):
        self.friends_controller.remove_friend(id)
        self.ui.friends_tab.populate_tree()
        self.save_config()

    def clear_friends(self):
        self.friends_controller.clear_friends()
        self.ui.friends_tab.populate_tree()
        self.save_config()

    def get_friends(self):
        return self.friends_controller.get_friends()

    def add_pet(self):
        print("MainController: add_pet called")
        self.pets_controller.add_pet()
        if self.ui:
            print("Updating UI pets tab")
            self.ui.pets_tab.populate_tree()
        else:
            print("UI not set, cannot update pets tab")
        self.save_config()

    def remove_pet(self, id):
        self.pets_controller.remove_pet(id)
        if self.ui:
            self.ui.pets_tab.populate_tree()
        self.save_config()

    def clear_pets(self):
        self.pets_controller.clear_pets()
        if self.ui:
            self.ui.pets_tab.populate_tree()
        self.save_config()

    def get_pets(self):
        return self.pets_controller.get_pets()

    def set_scripts_tab(self, scripts_tab):
        self.scripts_tab = scripts_tab

    def run_enabled_auto_functions(self):
        start_time = time.time()
        for category, functions in self.state.auto_functions.items():
            for func_name, func_data in functions.items():
                if func_data.get('enabled', False):
                    self.run_auto_function(func_name, loop=False, timeout=self.state.auto_functions_timeout)
        
        elapsed_time = (time.time() - start_time) * 1000
        if elapsed_time < self.state.auto_functions_timeout:
            sleep_time = (self.state.auto_functions_timeout - elapsed_time) / 1000
            time.sleep(sleep_time)

    def load_auto_functions(self):
        try:
            with open('auto_functions.json', 'r') as f:
                loaded_functions = json.load(f)
            
            self.state.auto_functions = loaded_functions
            print("Auto functions loaded successfully")
        except FileNotFoundError:
            print("No saved auto functions found. Starting with empty set.")
        except json.JSONDecodeError:
            print("Error decoding saved auto functions. Starting with empty set.")

    def execute_auto_function(self, function_name, *args):
        if function_name in self.auto_functions:
            return self.auto_functions[function_name](*args)
        else:
            print(f"Auto function '{function_name}' not found")

    def update_auto_function_param(self, function_name, new_param):
        if function_name in self.auto_functions:
            # Update the parameter for the specified auto function
            # This is a simplified example; you may need to adjust based on your specific needs
            self.auto_functions[function_name].__defaults__ = (new_param,)
        else:
            raise AttributeError(f"Auto function '{function_name}' not found")

    def check_stealth_connection(self):
        try:
            self.py_stealth.Self()  # This will attempt to connect to Stealth
            return True
        except SocketError as e:
            if e.errno == ECONNREFUSED:
                print("Connection to Stealth client failed. Please ensure Stealth is running.")
            else:
                print(f"An unexpected error occurred: {str(e)}")
            return False

    def reconnect_to_stealth(self, max_attempts=5, delay=2):
        for attempt in range(max_attempts):
            print(f"Attempting to reconnect to Stealth (attempt {attempt + 1}/{max_attempts})...")
            if self.check_stealth_connection():
                print("Successfully reconnected to Stealth.")
                return True
            time.sleep(delay)
        print("Failed to reconnect to Stealth after multiple attempts.")
        return False

    def _prepare_script_namespace(self):
        script_namespace = globals().copy()
        
        for name, func in globals().items():
            if callable(func) and not name.startswith('__'):
                script_namespace[name] = func
        
        import core.uo_globals
        for name, func in vars(core.uo_globals).items():
            if callable(func) and not name.startswith('__'):
                script_namespace[name] = func

        script_namespace['controller'] = self
        return script_namespace

    def initialize_stealth_connection(self):
        print("Initializing Stealth connection...")
        if self.check_stealth_connection():
            print("Successfully connected to Stealth.")
            return True
        else:
            print("Failed to connect to Stealth. Please ensure Stealth is running.")
            return False

    def main_loop(self):
        print("Entering main loop...")
        while True:
            if not self.check_stealth_connection():
                print("Lost connection to Stealth. Attempting to reconnect...")
                if not self.reconnect_to_stealth():
                    print("Failed to reconnect. Exiting main loop.")
                    break

            if self.state.auto_functions_enabled:
                self.run_enabled_auto_functions()

            # time.sleep(1)  # Adjust this value as needed
        
        print("Exiting main loop.")

    def save_auto_functions(self):
        serializable_auto_functions = {}
        for category, functions in self.state.auto_functions.items():
            serializable_auto_functions[category] = {}
            for func_name, func_data in functions.items():
                serializable_auto_functions[category][func_name] = {
                    'order': func_data.get('order', 0),
                    'enabled': func_data.get('enabled', False),
                    'hotkey': func_data.get('hotkey', ''),
                    'path': func_data.get('path', '')
                }

        with open('auto_functions.json', 'w') as f:
            json.dump(serializable_auto_functions, f, indent=2)

    def update_auto_functions_order(self, new_order):
        updated_auto_functions = {}
        for category, functions in self.state.auto_functions.items():
            updated_auto_functions[category] = {}
            for func_name in new_order:
                if func_name in functions:
                    updated_auto_functions[category][func_name] = functions[func_name]
        self.state.auto_functions = updated_auto_functions
        self.save_config()

    def start(self):
        self.hotkey_controller.start()  # Always start the listener
        # ... existing code ...

    def stop(self):
        if self.hotkey_controller.listener:
            pass
            # self.hotkey_controller.listener.stop()
        # ... existing code ...