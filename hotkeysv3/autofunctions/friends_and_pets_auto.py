from py_stealth import *
from utils import debug
from hotkey_config import HotkeyConfig

def main(enabled=False, threshold=70):
    debug(f"Friends and Pets auto function is {'enabled' if enabled else 'disabled'} (threshold: {threshold})", "info")
    
    if not enabled:
        return

    friends = HotkeyConfig.get_friends_list()
    pets = HotkeyConfig.get_pets_list()
    
    # Example: Heal friends if their health is below the threshold
    for friend_id, friend_name in friends:
        if IsObjectExists(int(friend_id)):
            friend_health = GetHP(int(friend_id))
            friend_max_health = GetMaxHP(int(friend_id))
            health_percentage = (friend_health / friend_max_health) * 100
            if health_percentage < threshold:
                debug(f"Healing friend {friend_name} (ID: {friend_id})", "info")
                Cast("Greater Heal")
                WaitTargetObject(int(friend_id))
                Wait(1000)
    
    # Example: Feed pets if they're hungry (assuming a hunger system)
    for pet_id, pet_name in pets:
        if IsObjectExists(int(pet_id)):
            # This is a placeholder function, replace with actual method to check pet hunger
            debug(f"Feeding pet {pet_name} (ID: {pet_id})", "info")
            UseObject(FindType(0x097B))  # Assuming 0x097B is the object ID for pet food
            WaitTargetObject(int(pet_id))
            Wait(1000)

    debug("Friends and Pets auto function cycle completed", "success")