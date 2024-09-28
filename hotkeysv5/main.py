from core.main_controller import MainController
from core.py_stealth import PyStealth

def main():
    py_stealth = PyStealth()
    try:
        controller = MainController(py_stealth)
        # Start your UI here if you have one
        # This will keep the script running
        controller.main_thread.join()
    except ConnectionError as e:
        print(f"Error: {e}")
    finally:
        print("Exiting script")

if __name__ == "__main__":
    main()