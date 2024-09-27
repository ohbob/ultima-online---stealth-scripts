import tkinter as tk
from tkinter import ttk

class PetsTab:
    def __init__(self, notebook, manager):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Pets")
        self.manager = manager

        self.tree = ttk.Treeview(self.frame, columns=('ID', 'Name'), show='headings')
        self.tree.heading('ID', text='Pet ID')
        self.tree.heading('Name', text='Pet Name')
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=5, padx=10, fill=tk.X)

        ttk.Button(button_frame, text="Add", command=self.add_pet).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove", command=self.remove_pet).pack(side=tk.LEFT, padx=5)

    def load_pets(self, pets):
        self.tree.delete(*self.tree.get_children())
        for pet_id, pet_name in pets:
            self.tree.insert('', 'end', values=(pet_id, pet_name))

    def add_pet(self):
        self.manager.debug("Please select a pet in the game.", "info")
        pet_id = self.manager.getTargetID()
        if pet_id:
            pet_name = self.manager.GetName(pet_id)
            # Check if the pet already exists in the list
            for item in self.tree.get_children():
                if self.tree.item(item)['values'][0] == pet_id:
                    self.manager.debug(f"Pet {pet_name} (ID: {pet_id}) already exists in the list.", "warning")
                    return
            self.tree.insert('', 'end', values=(pet_id, pet_name))
            self.manager.debug(f"Added pet: {pet_name} (ID: {pet_id})", "success")
            self.save_pets()
        else:
            self.manager.debug("Failed to get pet ID.", "error")

    def remove_pet(self):
        selected = self.tree.selection()
        if selected:
            pet_id, pet_name = self.tree.item(selected[0])['values']
            self.tree.delete(selected[0])
            self.manager.debug(f"Removed pet: {pet_name} (ID: {pet_id})", "info")
            self.save_pets()

    def save_pets(self):
        pets = [(self.tree.item(child)['values'][0], self.tree.item(child)['values'][1]) 
                for child in self.tree.get_children()]
        self.manager.update_pets_list(pets)