from py_stealth import *
from utils import debug, toggleable, exclude_from_gui, buff_exists, buffs_exist
from constants import CONSUMABLE_MAP, ConsumableType
from system_functions import SystemFunctions
import time
from collections import defaultdict


def handle_system_message(message):
    if "You finish applying the bandages" in message:
        debug("Finished bandaging!")
        SystemFunctions.reset_timer("bandage")
    # Add more message handling here if needed

def getTargetID():
        ClientRequestObjectTarget()
        WaitForClientTargetResponse(60000)
        if ClientTargetResponsePresent():
            response = ClientTargetResponse()
            if isinstance(response, dict):
                item_id = response.get('ID', None)
                return item_id
        return None

def consume(item: ConsumableType) -> bool:
        if item in CONSUMABLE_MAP:
            type, color = CONSUMABLE_MAP[item]
            if UseType(type, color):
                debug(f"Using {item}", "success")
                return True
            else:
                debug(f"MISSING {item}", "warning")
                return False
        else:
            debug(f"Unknown consumable: {item}", "warning")
            return False

def CastTo(spell, mana, id, timeout=2500):
    if spell and Mana() > mana:
        Cast(spell)
        WaitForTarget(timeout)
        if TargetPresent():
            TargetToObject(id)
            return True
    return False


class UserFunctions:
    @staticmethod
    def singleGetInfo(id=None):
        debug("Executing singleGetInfo", "info")
        if id is None:
            id = getTargetID()
            if id is None:
                debug("No target selected.", "info")
                return
        
        name = GetTooltip(id)
        info = f"Name: {name.split('|')[0]}, Type: {GetType(id)}, Color: {GetColor(id)}, ID: {id}"
        debug(info, "info", False)
    
    @staticmethod
    def containerGetInfo():
        debug("Executing containerGetInfo", "info")
        id = getTargetID()
        if id != None:
            FindType(0xFFFF, id)
            if GetFindedList():
                print("----------")
                for item in GetFindedList():
                    UserFunctions.singleGetInfo(item)
                print("----------")

    @staticmethod
    @toggleable(default=False, threshold=70)
    def auto_cast_heal_self():
        debug("Executing auto_cast_heal_self", "info")
        # debug(f"Auto heal enabled: {UserFunctions.auto_cast_heal_self.enabled}", "info")
        # debug(f"Current HP: {GetHP(Self())}, Max HP: {MaxHP()}, Threshold: {UserFunctions.auto_cast_heal_self.threshold}", "info")
        if UserFunctions.auto_cast_heal_self.enabled and not Dead() and GetHP(Self()) < (MaxHP() * UserFunctions.auto_cast_heal_self.threshold / 100):
            # debug("Attempting to cast heal", "info")
            UserFunctions.cast_heal_self()
        # else:
        #     debug("Conditions for auto heal not met", "info")

    @staticmethod
    @toggleable(default=False, threshold=99)
    def autobandage():
        if UserFunctions.autobandage.enabled and not Dead() and GetSkillCurrentValue("Healing") > 40 and not buffs_exist(['Veterinary', 'Healing']) and GetHP(Self()) <  (MaxHP() * UserFunctions.autobandage.threshold / 100):
            if UserFunctions.consume("BANDAGE") and WaitForTarget(500) and TargetPresent():
                TargetToObject(Self())
                debug("Bandaging self", "info")

    def animalform():
        if not Dead() and GetSkillValue("Ninjitsu") > 40 and Mana() > 15:
            Cast("Animal Form")


    @SystemFunctions.cooldown("heal", 100)  # 5 seconds in milliseconds
    def cast_heal_self():
        if GetSkillCurrentValue("Magery") > 40 and not Dead():
            if CastTo("Greater Heal", 15, Self()):
                return True
        return False

    def deconstruct_gump():
        for i in range(GetGumpsCount()):
            gump = GetGumpInfo(i)
            for entry in gump:
                debug(f"---------\n{entry}", "info")
                if len(entry) > 0:
                    subentries = gump[entry]
                    if isinstance(subentries, list):
                        for x in subentries:
                            debug(str(x), "info", False)
                    else:
                        debug(str(subentries), "info", False)

    def hide():
        if not Hidden():
            UseSkill('Hiding')
            debug("Not hidden", "warning")
        else:
            debug("Already hidden", "info")

    def cast_magic_arrow():
        debug("Casting Magic Arrow", "info")

    def cancel_target():
        if TargetPresent():
            CancelTarget()
            debug("Target Canceled", "warning")
    
    def get_total_stats(show_resistances=True, show_bonuses=True, show_damage=True, 
                        show_hit_effects=True, show_durability=False, show_other=True, show_items=True):
        target = getTargetID()
        if target is None:
            debug("No target selected.", "warning")
            return

        debug("---------", "info", False)
        debug(f"Stats for: {GetName(target)}", "info", False)

        items = [ObjAtLayerEx(layer, target) for layer in range(25) if ObjAtLayerEx(layer, target)]
        total_stats = defaultdict(float)

        for item in items:
            info = GetTooltip(item)
            for prop in info.split('|'):
                key, value = prop.rsplit(':', 1) if ':' in prop else prop.rsplit(' ', 1) if ' ' in prop else (None, None)
                if key and value:
                    try:
                        total_stats[key.strip().lower()] += float(value.strip().rstrip('%'))
                    except ValueError:
                        pass

        def normalize_stat_name(stat: str) -> str:
            stat = stat.lower().replace('total ', '')
            if 'durability' in stat:
                return 'durability'
            return stat

        def format_stat_value(stat: str, value: float) -> str:
            if 'resist' in stat or 'increase' in stat or 'reduction' in stat:
                return f"{value:.1f}%"
            if stat == 'durability':
                return f"{value:.0f}"
            if value == float('inf'):
                return "Infinite"
            if 'weapon damage' in stat:
                return f"{value:.0f}"
            return f"{value:.1f}"

        grouped_stats = defaultdict(dict)
        for stat, value in total_stats.items():
            normalized_stat = normalize_stat_name(stat)
            formatted_value = format_stat_value(normalized_stat, value)
            
            if 'resist' in normalized_stat:
                grouped_stats['Resistances'][normalized_stat] = formatted_value
            elif 'bonus' in normalized_stat or 'increase' in normalized_stat:
                grouped_stats['Bonuses'][normalized_stat] = formatted_value
            elif 'durability' in normalized_stat:
                grouped_stats['Durability'][stat] = formatted_value
            elif 'damage' in normalized_stat:
                if 'weapon damage' in normalized_stat:
                    parts = normalized_stat.split()
                    if len(parts) >= 3:
                        key = f"Weapon damage {parts[2]}"
                        grouped_stats['Damage'][key] = formatted_value
                else:
                    grouped_stats['Damage'][normalized_stat] = formatted_value
            elif 'hit' in normalized_stat:
                grouped_stats['Hit Effects'][normalized_stat] = formatted_value
            else:
                grouped_stats['Other'][normalized_stat] = formatted_value
        
        grouped_stats['Items'] = {f"Item {i+1}": GetTooltip(item).split('|')[0].strip() for i, item in enumerate(items)}
        
        sections_to_show = {
            'Resistances': show_resistances,
            'Bonuses': show_bonuses,
            'Damage': show_damage,
            'Hit Effects': show_hit_effects,
            'Durability': show_durability,
            'Other': show_other,
            'Items': show_items
        }

        order = ['Resistances', 'Bonuses', 'Damage', 'Hit Effects', 'Durability', 'Other', 'Items']
        for group in order:
            if group in grouped_stats and sections_to_show.get(group, True):
                debug(f"\n{group}:", "info", False)
                for stat, value in grouped_stats[group].items():
                    debug(f"  {stat.capitalize()}: {value}", "info", False)

        debug("---------", "info", False)


    @staticmethod
    @exclude_from_gui
    def main_loop():
        debug("Starting UserFunctions main_loop", "info")
        journal_index = HighJournal()
        last_toggle_check = time.time()
        toggle_check_interval = 0.2  # 200ms

        while True:
            try:
                current_time = time.time()
                if SystemFunctions.hotkeys_enabled:
                    # Only check toggles every 200ms
                    if current_time - last_toggle_check >= toggle_check_interval:
                        for func_name in dir(UserFunctions):
                            func = getattr(UserFunctions, func_name)
                            if callable(func) and hasattr(func, 'enabled') and func.enabled:
                                try:
                                    func()
                                except Exception as e:
                                    debug(f"Error in {func_name}: {str(e)}", "fail")
                        last_toggle_check = current_time

                # Check for new journal entries
                new_index = HighJournal()
                while journal_index < new_index:
                    message = Journal(journal_index)
                    handle_system_message(message)
                    journal_index += 1

                time.sleep(0.05)  # Small delay to prevent excessive CPU usage
            except Exception as e:
                debug(f"Error in main loop: {str(e)}", "fail")
                time.sleep(1)  # Add a delay before retrying to prevent rapid error loops

