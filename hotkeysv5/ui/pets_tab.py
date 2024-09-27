import tkinter as tk
from tkinter import ttk

class PetsTab(ttk.Frame):
    def __init__(self, parent, main_controller):
        super().__init__(parent)
        self.main_controller = main_controller
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=('Name', 'ID'), show='headings')
        self.tree.heading('Name', text='Name')
        self.tree.heading('ID', text='ID')
        self.tree.column('Name', width=150)
        self.tree.column('ID', width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        self.add_button = ttk.Button(button_frame, text="Add Pet", command=self.add_pet)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = ttk.Button(button_frame, text="Remove Pet", command=self.remove_pet)
        self.remove_button.pack(side=tk.LEFT, padx=5)
        self.clear_button = ttk.Button(button_frame, text="Clear Pets", command=self.clear_pets)
        self.clear_button.pack(side=tk.RIGHT, padx=5)

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        pets = self.main_controller.get_pets()
        for pet in pets:
            self.tree.insert('', 'end', values=(pet['name'], pet['id']))

    def add_pet(self):
        # Implement add pet functionality
        pass

    def remove_pet(self):
        # Implement remove pet functionality
        pass

    def clear_pets(self):
        # Implement clear pets functionality
        pass

    # ... (other methods as needed)