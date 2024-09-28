# from py_stealth import *

def main(main_controller):
    if not TargetPresent():
        pets = main_controller.get_pets()
        if not pets:
            ClientPrintEx(Self(), 1, 3, "No pets in the petlist.")
            return
        SetFindDistance(12) # max distance to target
        FindType(0xFFFF, Ground())
        found_pets = []
        pet_ids = [pet['id'] for pet in pets]  # Extract friend IDs
        for item in GetFoundList():
            if item in pet_ids:  # Compare by ID
                found_pets.append(item)

        if found_pets:
            closest_pet = min(found_pets, key=lambda x: GetDistance(x))
            TargetToObject(closest_pet)
            ClientPrintEx(closest_pet, 44, 3, f"TARGET")
            ClientPrintEx(closest_pet, 44, 3, "↓")
        else:
            ClientPrintEx(Self(), 1, 3, "No pets found nearby.")