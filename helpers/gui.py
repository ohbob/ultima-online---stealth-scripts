import tkinter as tk
import threading
import time
import configparser
# import atexit
import os
import sys
from tkinter import ttk

# Define global variables
toggle_states = {}
toggle_button = None
started = False
label_to_variable = {}
root = None
status = ""
status_label = None
timer_label = None
start_time = None

# Load configuration from file
config = configparser.ConfigParser()
config_filename = f'config_{os.path.splitext(os.path.basename(sys.argv[0]))[0]}.ini'
config.read(config_filename)


def update_variable_value(var_name, var_value):
    if var_name in variable_labels:
        variable_label, value_label = variable_labels[var_name]
        value_label.config(text=str(var_value))


variable_labels = {}
variable_label_frames = {}


# def create_vars(labels, variables, buttons):
#     global toggle_states, label_to_variable, root, status_label, timer_label
#
#     root = tk.Tk()
#     root.title("Camo gui builder")
#     root.geometry("200x440")  # Set default size
#
#     create_start_stop_row()  # Create Start/Stop button row
#
#     # VARIABLES ------------------
#     for var_name, var_value in variables:
#         variable_frame = tk.Frame(root)
#         variable_frame.pack(side=tk.TOP, fill=tk.X)
#
#         label = tk.Label(variable_frame, text=f"{var_name}: {var_value}", anchor="w", padx=4, pady=2)
#         label.pack(side=tk.LEFT, fill=tk.X, expand=True)
#
#         variable_labels[var_name] = label
#     # END VARIABLES --------------
#
#     # SEPARATOR ------------------
#     separator = ttk.Separator(root, orient='horizontal')
#     separator.pack(fill=tk.X, pady=5)
#     # END SEPARATOR --------------
#
#     # TOGGLE LABELS -------------
#     label_to_variable = {label: label.lower().replace(" ", "") for label in labels}
#
#     toggle_states = {label: tk.BooleanVar(value=config.getboolean('Toggles', variable, fallback=False))
#                      for label, variable in label_to_variable.items()}
#
#     toggle_frame = tk.Frame(root)
#     toggle_frame.pack(side=tk.TOP, fill=tk.X)
#
#     for i, label in enumerate(toggle_states.keys()):
#         if i % 2 == 0:
#             row_frame = tk.Frame(toggle_frame)
#             row_frame.pack(fill=tk.X)
#
#         toggle = tk.Checkbutton(row_frame, text=label, variable=toggle_states[label], anchor="w", padx=8, pady=5)
#         toggle.config(command=lambda l=label: toggle_function(l))
#         toggle.pack(side=tk.LEFT, fill=tk.X, expand=True)
#
#     # END TOGGLE LABELS ----------
#
#     # SEPARATOR ------------------
#     separator = ttk.Separator(root, orient='horizontal')
#     separator.pack(fill=tk.X, pady=5)
#     # END SEPARATOR --------------
#
#     # BUTTONS --------------------
#     button_frame = tk.Frame(root)
#     button_frame.pack(side=tk.TOP, fill=tk.X)
#
#     for i in range(0, len(buttons), 2):
#         row_frame = tk.Frame(button_frame)
#         row_frame.pack(fill=tk.X)
#
#         for button_text, button_callback in buttons[i:i + 2]:
#             button = tk.Button(row_frame, text=button_text, command=button_callback, padx=8, pady=5)
#             button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, pady=2)
#     # END BUTTONS ----------------
#
#     # TIMER ---------------------
#     timer_label = tk.Label(root, text="", anchor="w", padx=8, pady=5)
#     timer_label.pack(side=tk.TOP, fill=tk.X)
#     # END TIMER -----------------
#
#     # STATUS --------------------
#     status_label = tk.Label(root, text="Status: ", anchor="w", padx=8, pady=5)
#     status_label.pack(side=tk.TOP, fill=tk.X)
#     # END STATUS ----------------
#
#     update_status()  # Start status update loop
#
#     # root.mainloop()


def create_vars(labels, variables, buttons):
    global toggle_states, label_to_variable, root, status_label, timer_label

    root = tk.Tk()
    root.title("Camo gui builder")
    root.geometry("250x440")  # Set default size

    create_start_stop_row()  # Create Start/Stop button row

    # VARIABLES ------------------
    for var_name, var_value in variables:
        variable_frame = tk.Frame(root)
        variable_frame.pack(side=tk.TOP, fill=tk.X)

        label = tk.Label(variable_frame, text=f"{var_name}: {var_value}", anchor="w", padx=4, pady=2)
        label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        variable_labels[var_name] = label
    # END VARIABLES --------------

    # SEPARATOR ------------------
    separator = ttk.Separator(root, orient='horizontal')
    separator.pack(fill=tk.X, pady=5)
    # END SEPARATOR --------------

    # TOGGLE LABELS -------------
    label_to_variable = {label: label.lower().replace(" ", "") for label in labels}

    toggle_states = {label: tk.BooleanVar(value=config.getboolean('Toggles', variable, fallback=False))
                     for label, variable in label_to_variable.items()}

    toggle_frame = tk.Frame(root)
    toggle_frame.pack(side=tk.TOP, fill=tk.X)

    for i, label in enumerate(toggle_states.keys()):
        row = i // 2
        column = i % 2

        toggle = tk.Checkbutton(toggle_frame, text=label, variable=toggle_states[label], anchor="w", padx=8, pady=5)
        toggle.config(command=lambda l=label: toggle_function(l))
        toggle.grid(row=row, column=column, sticky=tk.W)

        toggle_frame.grid_columnconfigure(column, weight=1)  # Makes the columns take up equal space
    # END TOGGLE LABELS ----------

    # SEPARATOR ------------------
    separator = ttk.Separator(root, orient='horizontal')
    separator.pack(fill=tk.X, pady=5)
    # END SEPARATOR --------------

    # BUTTONS --------------------
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.TOP, fill=tk.X)

    max_button_width = max(len(text) for text, _ in buttons)

    for i in range(0, len(buttons), 2):
        row_frame = tk.Frame(button_frame)
        row_frame.pack(fill=tk.X)

        for j, (button_text, button_callback) in enumerate(buttons[i:i + 2]):
            button = tk.Button(row_frame, text=button_text, command=button_callback, padx=8, pady=5, width=max_button_width)
            button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, pady=2)

            row_frame.grid_columnconfigure(j, weight=1)  # Makes the columns take up equal space
    # END BUTTONS ----------------

    # TIMER ---------------------
    timer_label = tk.Label(root, text="", anchor="w", padx=8, pady=5)
    timer_label.pack(side=tk.TOP, fill=tk.X)
    # END TIMER -----------------

    # STATUS --------------------
    status_label = tk.Label(root, text="Status: ", anchor="w", padx=8, pady=5)
    status_label.pack(side=tk.TOP, fill=tk.X)
    # END STATUS ----------------

    update_status()  # Start status update loop


def save_config():
    config['Toggles'] = {variable: str(toggle_states[label].get()) for label, variable in label_to_variable.items()}

    with open(config_filename, 'w') as configfile:
        config.write(configfile)


def toggle_function(label):
    variable = label_to_variable[label]
    if toggle_states[label].get():
        globals()[variable] = True
        print(f"{label} is toggled ON")
    else:
        globals()[variable] = False
        print(f"{label} is toggled OFF")
    save_config()


def toggle_global():
    global started, start_time, status
    started = not started
    toggle_button.config(text="Stop" if started else "Start", bg="#8f8e95" if started else "#e7bb64")
    save_config()
    status = "Running" if started else "Stopped"  # Update status variable
    if started:
        start_time = time.time()
        update_timer()


def create_start_stop_row():
    global toggle_button
    toggle_button = tk.Button(root, text="Start", bg="#e7bb64", command=toggle_global)
    toggle_button.pack(side=tk.BOTTOM, fill=tk.X)  # Button at the bottom, takes the whole width


def update_status():
    global status
    status_text = f"Status: {status}"
    status_label.config(text=status_text)
    root.after(1000, update_status)


def update_timer():
    global start_time
    if started:
        elapsed_time = time.time() - start_time
        timer_text = format_time(elapsed_time)
        timer_label.config(text=timer_text)
        root.after(1000, update_timer)


def format_time(seconds):
    intervals = [
        ('weeks', 604800),
        ('days', 86400),
        ('hours', 3600),
        ('minutes', 60),
        ('seconds', 1)
    ]

    result = []

    for name, count in intervals:
        value = int(seconds) // count
        if value > 0:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append(f"{value} {name}")

    return ', '.join(result)


def update_variable_labels(variables):
    for var_name, var_value in variables:
        variable_labels[var_name].config(text=f"{var_name}: {var_value}")


def start_toggles_loop(callback):
    if callback is not None:
        toggle_thread = threading.Thread(target=callback, daemon=True)
        toggle_thread.start()

    update_status()  # Start status update loop


def create_gui(labels, variables, buttons, callback=None):
    create_vars(labels, variables, buttons)  # Call the create_vars function to create GUI elements

def run_gui():
    root.mainloop()
