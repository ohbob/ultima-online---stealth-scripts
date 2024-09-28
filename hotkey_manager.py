import tkinter as tk
from tkinter import ttk, messagebox
from pynput import keyboard
import json
import time
import os
import importlib.util
import sys
import threading

# Global variables
py_stealth = None

def init_py_stealth(stealth_instance):
    global py_stealth
    py_stealth = stealth_instance

# Try to import py_stealth
try:
    import py_stealth
    init_py_stealth(py_stealth)
    print("py_stealth imported successfully")
except ImportError:
    print("Warning: py_stealth module not found. Some functions may not work.")

def debug(message, level="info"):
    print(f"[{level.upper()}] {message}")

class HotkeyManager:
    def __init__(self, master):
        debug("Initializing HotkeyManager")
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
        self.auto_functions_enabled = True
        self.hotkey_listener = None

        self.create_widgets()
        self.load_config()
        self.start_hotkey_listener()
        debug("HotkeyManager initialized")

    def create_widgets(self):
        debug("Creating widgets")
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Import tab classes here
        from tabs.scripts_tab import ScriptsTab
        from tabs.auto_functions_tab import AutoFunctionsTab
        from tabs.friends_tab import FriendsTab
        from tabs.pets_tab import PetsTab

        self.scripts_tab = ScriptsTab(self.notebook, self)
        self.auto_functions_tab = AutoFunctionsTab(self.notebook, self)
        self.friends_tab = FriendsTab(self.notebook, self)
        self.pets_tab = PetsTab(self.notebook, self)
        debug("Widgets created")

    # ... (include all other methods from the HotkeyManager class)

    def run(self):
        debug("Starting main loop")
        self.master.mainloop()

def main_loop():
    while True:
        # Add any continuous checks or operations here
        time.sleep(0.1)  # Small delay to prevent excessive CPU usage

if __name__ == "__main__":
    debug("Starting application")
    root = tk.Tk()
    app = HotkeyManager(root)
    
    # Start the main loop in a separate thread
    main_thread = threading.Thread(target=main_loop, daemon=True)
    main_thread.start()
    
    try:
        debug("Running application")
        app.run()
    except Exception as e:
        debug(f"An error occurred: {str(e)}", "error")
    finally:
        debug("Application closed")