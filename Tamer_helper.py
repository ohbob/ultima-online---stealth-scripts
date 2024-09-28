import ast
from py_stealth import *
from helpers.gui import g
import threading
import time
from threading import Event
import datetime
import tkinter as tk

def buff_exists(name):
    if not name:
        return False
    for buff in GetBuffBarInfo():
        buff_name = GetClilocByID(buff['ClilocID1']).upper()
        if name.upper() in buff_name:
            return True
    return False

def buffs_exist(names):
    if not names:
        return False
    for buff in GetBuffBarInfo():
        buff_name = GetClilocByID(buff['ClilocID1']).upper()
        for name in names:
            if name.upper() in buff_name:
                return True
    return False


selected_friend = None
stop_event = Event()
is_running = False

# Add this at the top of your file with other global variables
discord_cooldowns = {}

def setup_gui():
    g.add("list", "Friends", [], height=3, command=on_friend_select)
    g.add("button", "Add Friend", add_friend)
    g.add("button", "Remove Friend", remove_friend)
    g.add("variable", "friends_list", "[]")
    g.add("variable", "enemies_list", "[]")
    g.add("variable", "started", False)

    auto_functions = [
        ("Auto Heal", "Heal Threshold", 70),
        ("Auto Bandage", "Bandage Threshold", 99),
        ("Auto Cure", "Cure Threshold", 60),
        ("Auto Discord", None, None),
        ("Auto Remove Mortal", None, None),
        ("Auto Nature's Fury", "NF Mana Threshold", 60),
        ("Auto Follow", "Follow Distance", 1)
    ]

    for func, threshold_name, default_value in auto_functions:
        g.add("toggle", func, lambda f=func: toggle_function(f))
        if threshold_name:
            g.add("entry", threshold_name, default_value)

    g.add("toggle", "Skip Self Bandage", lambda: toggle_function("Skip Self Bandage"))

    print(f"Debug: Initial Auto Bandage toggle state: {g.getval('toggle_Auto Bandage')}")

def toggle_function(func_name):
    current_state = g.getval(f"toggle_{func_name}")
    new_state = not current_state
    g.setval(f"toggle_{func_name}", new_state)
    
    if new_state:
        g.set_button_color(func_name, '#4CAF50')  # Green when toggled on
        g.set_button_text(func_name, f"{func_name} (On)")
    else:
        g.set_button_color(func_name, '#e7bb64')  # Original color when toggled off
        g.set_button_text(func_name, func_name)
    
    print(f"Debug: {func_name} toggled to {new_state}")

def get_friends():
    return ast.literal_eval(g.getval('friends_list') or "[]")

def get_enemies():
    return ast.literal_eval(g.getval('enemies_list') or "[]")

def on_friend_select(event):
    global selected_friend
    selection = g.get_list_selection("Friends")
    friends = get_friends()
    print(f"Selection: {selection}, Friends: {friends}")  # Debug print
    if selection and friends and len(selection) > 0:
        index = selection[0]
        if 0 <= index < len(friends):
            selected_friend = friends[index]
            print(f"Selected friend: {selected_friend}")  # Debug print
        else:
            print(f"Invalid selection index: {index}")  # Debug print
            selected_friend = None
            refresh_friends_list()  # Refresh the list instead of clearing selection
    else:
        selected_friend = None
        print("No friend selected")  # Debug print

def add_friend():
    add_friend_button = g.root.nametowidget(".Add Friend")
    add_friend_button.config(text="Adding...", state="disabled")
    threading.Thread(target=_add_friend_thread, args=(add_friend_button,), daemon=True).start()

def _add_friend_thread(button):
    try:
        ClientRequestObjectTarget()
        WaitForClientTargetResponse(60000)
        if ClientTargetResponsePresent():
            new_id = ClientTargetResponse().get('ID')
            if new_id:
                friends = get_friends()
                new_friend = (str(new_id), GetName(new_id))
                if new_friend not in friends:
                    friends.append(new_friend)
                    g.setval('friends_list', str(friends))
                    print(f"Added new friend: {new_friend}")  # Debug print
                    print(f"Updated friends list: {friends}")  # Debug print
                    g.root.after(0, refresh_friends_list)  # Schedule refresh on main thread
    finally:
        g.root.after(0, lambda: button.config(text="Add Friend", state="normal"))

def remove_friend():
    selected = g.get_list_selection("Friends")
    friends = get_friends()
    if selected and len(selected) > 0:
        index = selected[0]
        if 0 <= index < len(friends):
            removed_friend = friends.pop(index)
            g.setval('friends_list', str(friends))
            print(f"Removed friend: {removed_friend}")  # Debug print
            refresh_friends_list()  # Refresh immediately after removing
            time.sleep(0.1)  # Small delay to allow GUI to update
            if hasattr(g, 'root') and g.root:
                g.root.update_idletasks()  # Force GUI update
            # Instead of clearing the selection, we'll just refresh the list
            refresh_friends_list()
    else:
        print("No friend selected for removal")

def refresh_friends_list():
    if not hasattr(g, 'root') or not g.root:
        return
    
    def _refresh():
        friends = get_friends()
        friend_names = [f[1] for f in friends]
        g.set_list_items("Friends", friend_names)
        print(f"Friends list refreshed: {friend_names}")  # Debug print
        
        # Clear the global selected_friend if it's no longer in the list
        global selected_friend
        if selected_friend and selected_friend not in friends:
            selected_friend = None
            print("Selected friend cleared as it's no longer in the list")

    g.root.after(0, _refresh)

def toggle_start_stop():
    global is_running
    is_running = not is_running
    if is_running:
        g.setval('started', True)
        stop_event.clear()
        print("Script started")
    else:
        g.setval('started', False)
        stop_event.set()
        print("Script stopped")

def auto_heal():
    if not g.getval('started') or not g.getval('toggle_Auto Heal'): return
    threshold = int(g.get_entry('Heal Threshold') or 70)
    friends = get_friends()
    friends.append((str(Self()), 'Self'))  # Add yourself to the list of friends to heal
    for friend_id, name in friends:
        friend_id = int(friend_id)
        if GetDistance(friend_id) >= 10 and friend_id != Self(): continue
        hp = GetHP(friend_id)
        if hp <= 0: continue  # Skip if target has 0 or negative health
        hp_percent = (hp * 100) / GetMaxHP(friend_id)  # Calculate actual percentage
        if hp_percent < threshold and not IsPoisoned(friend_id):
            print(f"Attempting to heal {name} (ID: {friend_id}), HP: {hp_percent}%")
            if GetSkillValue("Magery") > 50 and Mana() > 10:
                Cast("Greater Heal")
            elif GetSkillValue("Chivalry") > 50 and Mana() > 10:
                Cast("Close Wounds")
            else: continue
            WaitForTarget(1000)
            if TargetPresent():
                TargetToObject(friend_id)
                Wait(500)
            print(f"Heal cast on {name}")
            return True  # Return True if healing was attempted
    return False  # Return False if no healing was needed

def auto_bandage():
    if not g.getval('started') or not g.getval('toggle_Auto Bandage'):
        return False

    if buffs_exist(['Veterinary', 'Healing']):
        print("Bandaging in progress, skipping")
        return False

    threshold = int(g.get_entry('Bandage Threshold') or 99)
    skip_self = g.getval('toggle_Skip Self Bandage')
    friends = get_friends()
    friends.append((str(Self()), 'Self'))  # Add yourself to the list of friends to bandage

    for friend_id, name in friends:
        friend_id = int(friend_id)
        if skip_self and friend_id == Self():
            continue
        if GetDistance(friend_id) > 3 or IsYellowHits(friend_id):
            continue
        hp = GetHP(friend_id)
        if hp <= 0:
            continue
        hp_percent = (hp * 100) / GetMaxHP(friend_id)
        if hp_percent < threshold and not IsPoisoned(friend_id):
            print(f"Attempting to bandage {name} (ID: {friend_id}), HP: {hp_percent}%")
            UseType2(0x0E21)
            WaitForTarget(1000)
            if TargetPresent():
                TargetToObject(friend_id)
                Wait(500)  # Wait after targeting
                print(f"Bandage applied to {name}")
                return True
    return False

def auto_cure():
    if not g.getval('started') or not g.getval('toggle_Auto Cure'): return
    cure_threshold = int(g.get_entry('Cure Threshold') or 50)
    for friend_id, name in get_friends():
        friend_id = int(friend_id)
        if GetDistance(friend_id) >= 10 or IsYellowHits(friend_id): continue
        if IsPoisoned(friend_id):
            hp_percent = GetHP(friend_id) * (4 if friend_id != Self() else 1)
            if hp_percent <= cure_threshold:
                if GetSkillValue("Magery") > 50:
                    Cast("Cure")
                elif GetSkillValue("Chivalry") > 50:
                    Cast("Cleanse by Fire")
                WaitForTarget(100)
                if TargetPresent():
                    TargetToObject(friend_id)
                return

def find_enemies():
    SetFindDistance(12)
    FindType(0xFFFF, Ground())
    enemies = []
    friends_ids = [int(f[0]) for f in get_friends()]  # Convert friend IDs to integers
    for mobile in GetFindedList():
        if (GetDistance(mobile) <= 10 and 
            GetNotoriety(mobile) >= 3 and 
            mobile not in friends_ids and
            mobile != Self()):  # Exclude self
            enemies.append((str(mobile), GetName(mobile)))
    return enemies

def auto_discord():
    if not g.getval('started') or not g.getval('toggle_Auto Discord'):
        return
    enemies = find_enemies()
    print(f"Found enemies: {enemies}")
    current_time = time.time()
    for enemy_id, name in enemies:
        enemy_id = int(enemy_id)
        # Check if the enemy is on cooldown
        if enemy_id in discord_cooldowns and current_time - discord_cooldowns[enemy_id] < 30:
            print(f"Skipping {name} (ID: {enemy_id}) - on Discord cooldown")
            continue
        distance = GetDistance(enemy_id)
        print(f"Checking enemy {name} (ID: {enemy_id}), distance: {distance}")
        if distance <= 6 and "nature's fury" not in name.lower():
            print(f"Attempting to use Discord on {name}")
            start_time = datetime.datetime.now()
            UseSkill('Discordance')
            WaitForTarget(200)
            if TargetPresent():
                TargetToObject(enemy_id)
                Wait(100)  # Wait a bit longer for the journal message
            
            # Check for success or already discorded
            if InJournalBetweenTimes('You play successfully', start_time, datetime.datetime.now()) != -1:
                discord_cooldowns[enemy_id] = current_time
                print(f"Discord successful on {name} (ID: {enemy_id}). Cooldown started.")
                return
            elif InJournalBetweenTimes('creature is already in discord', start_time, datetime.datetime.now()) != -1:
                discord_cooldowns[enemy_id] = current_time
                print(f"{name} (ID: {enemy_id}) is already in discord. Cooldown started.")
                return
            elif InJournalBetweenTimes('but fail', start_time, datetime.datetime.now()) != -1:
                print(f"Discord failed on {name} (ID: {enemy_id}).")
            elif InJournalBetweenTimes('too far away', start_time, datetime.datetime.now()) != -1:
                print(f"Target {name} (ID: {enemy_id}) too far away for Discord.")
            else:
                print(f"Discord attempt on {name} (ID: {enemy_id}) timed out or unknown result.")
    print("No suitable targets for Discord found")

# Add this function to clean up old cooldowns
def clean_discord_cooldowns():
    current_time = time.time()
    global discord_cooldowns
    discord_cooldowns = {k: v for k, v in discord_cooldowns.items() if current_time - v < 30}

def remove_mortal():
    if not g.getval('started') or not g.getval('toggle_Auto Remove Mortal'): return
    for friend_id, name in get_friends():
        friend_id = int(friend_id)
        if GetDistance(friend_id) < 10 and IsYellowHits(friend_id):
            if GetSkillValue("Chivalry") > 50 and Mana() > 10:
                Cast("Remove Curse")
                WaitForTarget(200)
                if TargetPresent():
                    TargetToObject(friend_id)
                return

def auto_natures_fury():
    if not g.getval('started') or not g.getval('toggle_Auto Nature\'s Fury'): return
    enemies = find_enemies()
    if enemies:
        Cast('nature fury')
        WaitTargetXYZ(GetX(Self()), GetY(Self()) + 1, GetZ(Self()))

def auto_follow():
    if not g.getval('started') or not g.getval('toggle_Auto Follow') or not selected_friend: return
    friend_id = int(selected_friend[0])
    follow_distance = int(g.get_entry('Follow Distance') or 1)
    if GetDistance(friend_id) > follow_distance:
        NewMoveXY(GetX(friend_id), GetY(friend_id), True, 1, True)

def main_loop():
    while not Dead():
        if stop_event.is_set():
            time.sleep(1)
            continue
        try:
            if auto_heal():  # Prioritize healing
                continue  # Skip other actions if healing was performed
            if auto_bandage():  # Check if bandaging was performed
                print("Bandaging performed, skipping other actions")
                continue  # Skip other actions if bandaging was performed
            auto_cure()
            auto_discord()
            remove_mortal()
            auto_natures_fury()
            auto_follow()
            clean_discord_cooldowns()  # Add this line
        except Exception as e:
            print(f"Error in main loop: {e}")
        Wait(100)

def run():
    setup_gui()
    g.create_gui()  # This will initialize the root object
    
    # Now that the GUI is created, we can set initial values
    auto_functions = [
        "Auto Heal", "Auto Bandage", "Auto Cure", "Auto Discord",
        "Auto Remove Mortal", "Auto Nature's Fury", "Auto Follow"
    ]
    for func in auto_functions:
        g.setval(f"toggle_{func}", False)
    g.setval("toggle_Skip Self Bandage", False)
    
    refresh_friends_list()
    g.setval('started', False)
    threading.Thread(target=main_loop, daemon=True).start()
    g.run_gui()

if __name__ == "__main__":
    run()
