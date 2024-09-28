from py_stealth import *

while True:
    if Mana() > 5:
        CastToObj("Bless", 0x001DB4BF)
        Wait(2000)
    else:
        Wait(1000)
