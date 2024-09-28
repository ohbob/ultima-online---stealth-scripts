import tkinter as tk
from hotkey_config import HotkeyConfig
from utils import debug
import traceback
import threading
import time

def main_loop():
    while True:
        # Add any continuous checks or operations here
        time.sleep(0.1)  # Small delay to prevent excessive CPU usage

if __name__ == "__main__":
    try:
        debug("Starting application", "info")
        root = tk.Tk()
        debug("Tkinter root created", "info")
        app = HotkeyConfig(root)
        debug("HotkeyConfig instance created", "info")
        
        # Add a test hotkey
        app.config['test_function'] = {"hotkey": "<ctrl>+z"}
        app.ui.tree.insert('', 'end', values=('test_function', '<ctrl>+z'))
        app.functions['test_function'] = lambda config: debug("Test function activated!", "success")
        
        app.start_hotkey_listener()
        debug("Hotkey listener started", "info")

        # Start the main loop in a separate thread
        main_thread = threading.Thread(target=main_loop, daemon=True)
        main_thread.start()

        debug("Entering main loop", "info")
        root.mainloop()
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}\n{traceback.format_exc()}"
        debug(error_msg, "fail")
    finally:
        debug("Application closed", "info")