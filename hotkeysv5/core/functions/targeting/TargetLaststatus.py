# from py_stealth import *
def main():
    if TargetPresent():
        # ClientPrintEx(LastTarget(), 44, 3, f"LTARGET")
        TargetToObject(LastStatus())
        ClientPrintEx(LastStatus(), 44, 3, "↓")