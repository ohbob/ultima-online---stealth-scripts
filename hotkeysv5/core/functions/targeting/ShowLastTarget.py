# from py_stealth import *
def main():
    SetFindDistance(24)
    FindType(0xFFFF, Ground())
    items = GetFoundList()
    
    targets = {
        "LTARGET": LastTarget(),
        "LATTACK": LastAttack(),
        "LSTATUS": LastStatus()
    }
    
    for label, target in targets.items():
        if target in items:
            ClientPrintEx(target, 44, 3, f"{label}\n↓")