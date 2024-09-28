from py_stealth import *

SetContextMenuHook(ObjAtLayer(RhandLayer()), 0)
while GetSkillValue('Ninjitsu') < GetSkillCap('Ninjitsu'):
    RequestContextMenu(ObjAtLayer(RhandLayer()))
    WaitForTarget(2000)
    if TargetPresent():
        TargetToObject(FindTypeEx(0x2806, 0xFFFF, Backpack(), False))
    UseObject(ObjAtLayer(RhandLayer()))
    WaitForTarget(2000)
    if TargetPresent():
        TargetToObject(FindType(0x0115, Ground()))
