from core.py_stealth import *

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