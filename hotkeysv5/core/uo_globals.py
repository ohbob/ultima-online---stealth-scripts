from core.py_stealth import *
import time

def getTargetID(py_stealth):
    py_stealth.ClientRequestObjectTarget()
    py_stealth.WaitForClientTargetResponse(60000)
    if py_stealth.ClientTargetResponsePresent():
        response = py_stealth.ClientTargetResponse()
        if isinstance(response, dict):
            item_id = response.get('ID', None)
            return item_id
    return None

def debug(py_stealth, message: str, level: str = "info", client=True):
    color_map = {
        "success": 60,  # Green
        "fail": 30,     # Red
        "info": 10,      # Blue
        "warning": 40   # Orange
    }
    if client:
        py_stealth.ClientPrintEx(py_stealth.Self(), color_map[level], 1, f"* {message.upper()} *")
    print(message)

def use_skill(skill_name, target_self=False, gump_action=None, gump_timeout=1):
    if GetSkillValue(skill_name) < GetSkillCap(skill_name):
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
        # Wait(1000)