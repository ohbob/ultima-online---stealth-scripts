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

        if not self.initialize_stealth_connection():
            raise ConnectionError("Failed to initialize Stealth connection")

        self.main_thread = threading.Thread(target=self.main_loop)
        self.main_thread.daemon = True
        self.main_thread.start()

    def set_ui(self, ui):
        self.ui = ui
        if hasattr(ui, 'scripts_tab'):
            self.scripts_tab = ui.scripts_tab
        self.update_ui_with_discovered_functions()  # Update UI after it's set

    def set_hotkey(self, func_name):
        # This should be implemented in the HotkeysController
        self.hotkeys_controller.set_hotkey(func_name)
        print(f"Hotkey set for function: {func_name}")
        self.print_current_state()

    def clear_hotkey(self, func_name):
        # This should be implemented in the HotkeysController
        self.hotkeys_controller.clear_hotkey(func_name)
        print(f"Hotkey cleared for function: {func_name}")
        self.print_current_state()

    def run_once(self, func_name):
        print(f"Running function once: {func_name}")
        self.run_script(func_name, loop=False, timeout=self.state.scripts_timeout)

    def set_scripts_timeout(self, timeout):
        try:
            timeout = int(timeout)
            self.state.set_scripts_timeout(timeout)
            print(f"Scripts timeout set to: {timeout} ms")
            self.print_current_state()
        except ValueError:
            print("Invalid timeout value. Please enter a valid integer.")

    def set_auto_functions_timeout(self, timeout):
        try:
            timeout = int(timeout)
            self.state.set_auto_functions_timeout(timeout)
            print(f"Auto functions timeout set to: {timeout} ms")
            self.print_current_state()
        except ValueError:
            print("Invalid timeout value. Please enter a valid integer.")

    def toggle_all_auto_functions(self):
        new_state = not self.state.auto_functions_enabled
        self.state.set_auto_functions_enabled(new_state)
        self.auto_functions_controller.set_all_auto_functions_state(new_state)
        print(f"Auto functions {'enabled' if new_state else 'disabled'}")
        self.print_current_state()
        if self.ui and hasattr(self.ui, 'auto_functions_tab'):
            self.ui.auto_functions_tab.update_auto_button_state(new_state)
        return new_state

    def toggle_all_hotkeys(self):
        self.hotkeys_enabled = not self.hotkeys_enabled
        # ... logic to enable/disable hotkeys ...
        if self.scripts_tab:
            self.scripts_tab.update_hotkey_button_state(self.hotkeys_enabled)
        return self.hotkeys_enabled

    def save_config(self):
        # Implement saving configuration
        pass

    def load_config(self):
        # Implement loading configuration
        pass

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

    def set_hotkeys_state(self, enabled):
        self.state.set_hotkeys_enabled(enabled)
        self.hotkeys_controller.set_all_hotkeys_state(enabled)
        print(f"Hotkeys {'enabled' if enabled else 'disabled'}")
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
                self.save_auto_functions()  # Save the updated state
                return
        print(f"Auto function '{func_name}' not found")

    def add_friend(self):
        self.friends_controller.add_friend()
        self.ui.friends_tab.populate_tree()

    def remove_friend(self, id):
        self.friends_controller.remove_friend(id)
        self.ui.friends_tab.populate_tree()

    def clear_friends(self):
        self.friends_controller.clear_friends()
        self.ui.friends_tab.populate_tree()

    def get_friends(self):
        return self.friends_controller.get_friends()

    def add_pet(self):
        print("MainController: add_pet called")  # Debug print
        self.pets_controller.add_pet()
        if self.ui:
            print("Updating UI pets tab")  # Debug print
            self.ui.pets_tab.populate_tree()
        else:
            print("UI not set, cannot update pets tab")  # Debug print

    def remove_pet(self, id):
        self.pets_controller.remove_pet(id)
        if self.ui:
            self.ui.pets_tab.populate_tree()

    def clear_pets(self):
        self.pets_controller.clear_pets()
        if self.ui:
            self.ui.pets_tab.populate_tree()

    def get_pets(self):
        return self.pets_controller.get_pets()

    def set_scripts_tab(self, scripts_tab):
        self.scripts_tab = scripts_tab

    def set_hotkeys_state(self, state):
        self.state.set_hotkeys_enabled(state)
        self.hotkeys_controller.set_all_hotkeys_state(state)
        print(f"Hotkeys {'enabled' if state else 'disabled'}")
        self.print_current_state()

    def set_loop_state(self, enabled):
        self.state.set_loop_enabled(enabled)
        print(f"Loop {'enabled' if enabled else 'disabled'}")
        self.print_current_state()

    def run_enabled_auto_functions(self):
        start_time = time.time()
        ordered_functions = []
        for category, functions in self.state.auto_functions.items():
            for func_name, func_data in functions.items():
                if func_data.get('enabled', False):
                    ordered_functions.append((func_name, func_data))
        
        # Sort the functions based on their order
        ordered_functions.sort(key=lambda x: x[1].get('order', 0))

        for func_name, func_data in ordered_functions:
            print(f"Running auto function: {func_name}")
            self.run_auto_function(func_name, loop=False, timeout=self.state.auto_functions_timeout)
        
        elapsed_time = (time.time() - start_time) * 1000
        if elapsed_time < self.state.auto_functions_timeout:
            sleep_time = (self.state.auto_functions_timeout - elapsed_time) / 1000
            print(f"Sleeping for {sleep_time:.2f} seconds")
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

            time.sleep(1)  # Adjust this value as needed
        
        print("Exiting main loop.")

    def save_auto_functions(self):
        print("Saving auto functions...")
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
        print("Auto functions saved")
        
        # Debug: print the contents of the saved file
        with open('auto_functions.json', 'r') as f:
            print("Saved auto functions:")
            print(f.read())

    def update_auto_function_order(self, func_name, order):
        for category, functions in self.state.auto_functions.items():
            if func_name in functions:
                functions[func_name]['order'] = order
                break