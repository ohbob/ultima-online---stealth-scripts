from core.uo_globals import debug, getTargetID

class PetsController:
    def __init__(self, state, py_stealth):
        self.state = state
        self.py_stealth = py_stealth

    def add_pet(self):
        print("PetsController: add_pet called")  # Debug print
        debug(self.py_stealth, "Select a pet to add")
        target_id = getTargetID(self.py_stealth)
        print(f"Target ID: {target_id}")  # Debug print
        if target_id:
            name = self.py_stealth.GetName(target_id)
            print(f"Pet name: {name}")  # Debug print
            if not name and self.py_stealth.GetHP(target_id) <= 0:
                debug(self.py_stealth, "Target is not a valid pet or is dead", "fail")
                return
            if any(pet['id'] == target_id for pet in self.state.pets):
                debug(self.py_stealth, f"Pet {name} is already in the list", "fail")
            else:
                pet = {'name': name, 'id': target_id}
                self.state.pets.append(pet)
                self.state.update_pets(self.state.pets)
                debug(self.py_stealth, f"Added pet: {name}, {target_id}", "success")
                print(f"Pet added: {pet}")  # Debug print
        else:
            debug(self.py_stealth, "No target selected")

    def remove_pet(self, id):
        pet_to_remove = next((pet for pet in self.state.pets if pet['id'] == id), None)
        if pet_to_remove:
            self.state.pets.remove(pet_to_remove)
            self.state.update_pets(self.state.pets)
            debug(self.py_stealth, f"Removed pet: {pet_to_remove['name']}, {id}", "success")
        else:
            debug(self.py_stealth, f"No pet with id {id} found", "fail")

    def clear_pets(self):
        self.state.pets = []
        self.state.update_pets(self.state.pets)

    def get_pets(self):
        return self.state.pets