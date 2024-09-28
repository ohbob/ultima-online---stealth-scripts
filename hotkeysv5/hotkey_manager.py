import tkinter as tk
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import py_stealth and create a single instance
import core.py_stealth as py_stealth
py_stealth_instance = py_stealth

from core.main_controller import MainController
from ui.main_ui import MainUI

def main():
    root = tk.Tk()
    main_controller = MainController(py_stealth_instance)
    main_ui = MainUI(root, main_controller)
    main_controller.set_ui(main_ui)
    main_controller.start()  # This will start the hotkey controller if enabled
    root.mainloop()

if __name__ == "__main__":
    main()
