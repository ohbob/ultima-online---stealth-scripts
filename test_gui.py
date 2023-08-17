import time

from helpers import gui


# Define the functions for the buttons
def button_a():
    print("Button A pressed")
    # Add your code here for what should happen when Button A is pressed


def button_b():
    print("Button B pressed")
    # Add your code here for what should happen when Button B is pressed


def button_c():
    print("Button C pressed")
    # Add your code here for what should happen when Button C is pressed


def button_d():
    print("Button D pressed")
    # Add your code here for what should happen when Button D is pressed


# Define the labels you want to use
gui_labels = [
    "Label 1",
    "Label 2",
    "Label 3",
    "Label 4",
    "Label 5",
]

a, b, c, d = "Random Script v1", 2, 3, 4

# Define the variables you want to display on the GUI
gui_variables = [
    ("a", a),
    ("b", b),
    ("c", c),
    ("d", d)
]

# Define the buttons and their corresponding callback functions
gui_buttons = [
    ("BUTTON A", button_a),
    ("BUTTON B", button_b),
    ("BUTTON C", button_c),
    ("BUTTON D", button_d)
]


def custom_callback():
    while True:
        time.sleep(0.5)
        if gui.started:
            if gui.toggle_states["Label 1"].get():
                print("Label 1 active")
                gui.update_variable_labels([("b", a)])
                gui.status = "First toggle activated"
            if gui.toggle_states["Label 2"].get():  
                print("Label 2 active")
            if gui.toggle_states["Label 3"].get():
                print("Label 3 active")
            if gui.toggle_states["Label 4"].get():
                print("Label 4 active")
            if gui.toggle_states["Label 5"].get():
                print("Label 5 active")


# Create the GUI and start the toggles loop
gui.create_gui(gui_labels, gui_variables, gui_buttons)  # Pass the custom callback function to start_toggles_loop
gui.update_variable_labels(gui_variables)  # Start updating variable labels
gui.start_toggles_loop(custom_callback)
gui.run_gui()
