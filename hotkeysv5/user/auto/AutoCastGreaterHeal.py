# from py_stealth import *

def main(hp=99):
    try:
        hp_value = int(hp)
    except ValueError:
        print(f"Invalid hp value: {hp}")
        hp_value = 99  # Default value if conversion fails
    
    print(f"HP threshold: {hp_value}")
    
    if not Dead() and not IsPoisoned(Self()) and GetHP(Self()) < hp_value and Mana() > 20:
        Cast("Greater Heal")
        WaitForTarget(2000)
        if TargetPresent():
            TargetToObject(Self())
            Wait(1000)

            
    # # UOSay(f"{v1} {v2} {v3}")
    # ClientPrintEx(Self(), 1, 3, f"AutoHeal: {hp} {mana} {stamina}")
    # # print("AutoHeal")
    # # ClientPrintEx(Self(), 1, 3, "Auto heal baby")