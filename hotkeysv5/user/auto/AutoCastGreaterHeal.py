# from py_stealth import *

def main():
    hp_percentage = 0.9  # 90% of MaxHP
    if not Dead() and not IsPoisoned(Self()) and GetHP(Self()) < (MaxHP() * hp_percentage) and Mana() > 20:
        Cast("Greater Heal")
        WaitForTarget(2000)
        if TargetPresent():
            TargetToObject(Self())