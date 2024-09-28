from py_stealth import *
while True:
    if Mana() > 20:
        # CastToObj("paralyze field", Self())
        CastToObj("energy field", Self())
        Wait(1500)
