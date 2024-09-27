def main(manager):
    pets = manager.get_pets_list()
    manager.debug("Pets list:", "info")
    for pet_id, pet_name in pets:
        manager.debug(f"ID: {pet_id}, Name: {pet_name}", "info")
        # You can add more functionality here, like:
        # UseObject(pet_id)
        # or any other action you want to perform with pets