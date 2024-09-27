class PetsController:
    def __init__(self, state):
        self.state = state
        self.pets = []

    def add_pet(self, pet):
        self.pets.append(pet)
        self.state.update_pets(self.pets)

    def remove_pet(self, pet):
        if pet in self.pets:
            self.pets.remove(pet)
            self.state.update_pets(self.pets)

    def get_pets(self):
        return self.pets

    # Add other pet-related methods