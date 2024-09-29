import tkinter as tk
import sys
import os
import logging

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import py_stealth and create a single instance
import core.py_stealth as py_stealth
py_stealth_instance = py_stealth

from core.main_controller import MainController
from ui.main_ui import MainUI

def main():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("Starting main application")

    root = tk.Tk()
    main_controller = MainController(py_stealth_instance)
    main_ui = MainUI(root, main_controller)
    main_controller.set_ui(main_ui)
    
    # Create a separate thread for handling hotkeys and script execution
    import threading
    hotkey_thread = threading.Thread(target=main_controller.run_hotkey_loop, daemon=True)
    hotkey_thread.start()
    
    logger.info("Main UI started. Press Ctrl+D to toggle hotkeys.")
    root.mainloop()

if __name__ == "__main__":
    main()
