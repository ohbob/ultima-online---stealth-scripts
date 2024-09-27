import tkinter as tk
from tkinter import ttk

class PetsTab(ttk.Frame):
    def __init__(self, parent, main_controller):
        super().__init__(parent)
        self.main_controller = main_controller
        self.create_widgets()

    def create_widgets(self):
        self.pets_listbox = tk.Listbox(self)
        self.pets_listbox.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        self.add_button = ttk.Button(button_frame, text="Add Pet", command=self.add_pet)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = ttk.Button(button_frame, text="Remove Pet", command=self.remove_pet)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(button_frame, text="Clear List", command=self.clear_list)
        self.clear_button.pack(side=tk.LEFT, padx=5)

    def add_pet(self):
        self.main_controller.add_pet()

    def remove_pet(self):
        selected = self.pets_listbox.curselection()
        if selected:
            pet = self.pets_listbox.get(selected[0])
            self.main_controller.remove_pet(pet)

    def clear_list(self):
        self.main_controller.clear_pets()
        self.populate_list()

    def populate_list(self):
        self.pets_listbox.delete(0, tk.END)
        pets = self.main_controller.get_pets()
        for pet in pets:
            self.pets_listbox.insert(tk.END, pet)