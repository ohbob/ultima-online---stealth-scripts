import time

def main(main_controller):
    start_time = time.time()  # Start timing

    if not TargetPresent():
        pets = main_controller.get_pets()
        if not pets:
            ClientPrintEx(Self(), 1, 3, "No pets in the petlist.")
            elapsed_time = (time.time() - start_time) * 1000  # Calculate elapsed time in ms
            print(f"Execution time: {elapsed_time:.4f} ms")
            return

        SetFindDistance(12)  # max distance to target
        FindType(0xFFFF, Ground())
        pet_ids = {pet['id'] for pet in pets}  # Use a set for faster lookup
        found_pets = []

        for item in GetFoundList():
            if item in pet_ids:
                hp = GetHP(item)
                if hp > 0 and hp < 25:  # Check if HP is larger than 0 but smaller than 25
                    found_pets.append((item, hp, GetDistance(item)))  # Store item, HP, and distance

        if found_pets:
            # Sort by HP (ascending) and then by distance (ascending)
            closest_pet = min(found_pets, key=lambda x: (x[1], x[2]))[0]
            TargetToObject(closest_pet)
            ClientPrintEx(closest_pet, 44, 3, f"TARGET")
            ClientPrintEx(closest_pet, 44, 3, "↓")
        else:
            ClientPrintEx(Self(), 1, 3, "No injured pets found nearby.")

    elapsed_time = (time.time() - start_time) * 1000  # Calculate elapsed time in ms
    ClientPrintEx(Self(), 1, 3, f"Execution time: {elapsed_time:.4f} ms")