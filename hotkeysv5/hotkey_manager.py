import tkinter as tk
from core.main_controller import MainController
from ui.main_ui import MainUI

def main():
    root = tk.Tk()
    main_controller = MainController()
    main_ui = MainUI(root, main_controller)
    main_controller.set_ui(main_ui)
    root.mainloop()

if __name__ == "__main__":
    main()
