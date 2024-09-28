from py_stealth import *
import time

def train_skill(skill_name, target_self=False, gump_action=None, gump_timeout=1):
    while GetSkillValue(skill_name) < GetSkillCap(skill_name):
        UseSkill(skill_name)
        if target_self:
            WaitTargetSelf()
        if gump_action:
            gump_id, button = gump_action
            start_time = time.time()
            while GetGumpID(0) != gump_id and time.time() - start_time < gump_timeout:
                Wait(100)
            if GetGumpID(0) == gump_id:
                NumGumpButton(0, button)
        Wait(1000)

train_skill("Tracking", gump_action=(2976808305, 3))
train_skill("Detect Hidden", target_self=True)
train_skill("Hiding")
