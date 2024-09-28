from py_stealth import *
from functools import wraps
import inspect
from typing import Literal
import logging
import os
from datetime import datetime

# Set up logging
logging.basicConfig(filename='hotkey_debug.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s: %(message)s')

def debug(message: str, level: str = "info", client=True) -> None:
    color_map = {
        "success": 60,  # Green
        "fail": 30,     # Red
        "info": 10,      # Blue
        "warning": 40   # Orange
    }
    if client:
        ClientPrintEx(Self(), color_map[level], 1, f"* {message.upper()} *")
    print(message)
    
    # Log to file
    if level == "success":
        logging.info(message)
    elif level == "fail":
        logging.error(message)
    elif level == "warning":
        logging.warning(message)
    else:
        logging.info(message)

def configurable_function(func):
    params = inspect.signature(func).parameters
    config = {name: param.default for name, param in params.items()}
    func.config = config
    return func

def exclude_from_gui(func):
    func._exclude_from_gui = True
    return func

def toggleable(default=False, **kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if wrapper.enabled:
                return func(*args, **kwargs)
        
        wrapper.enabled = default
        for key, value in kwargs.items():
            setattr(wrapper, key, value)
        
        def toggle():
            wrapper.enabled = not wrapper.enabled
            return wrapper.enabled
        
        wrapper.toggle = toggle
        return wrapper
    return decorator

def buff_exists(name):
    if not name:
        return False
    for buff in GetBuffBarInfo():
        buff_name = GetClilocByID(buff['ClilocID1']).upper()
        if name.upper() in buff_name:
            return True
    return False

def buffs_exist(names):
    if not names:
        return False
    for buff in GetBuffBarInfo():
        buff_name = GetClilocByID(buff['ClilocID1']).upper()
        for name in names:
            if name.upper() in buff_name:
                return True
    return False

def setup_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"error_log_{timestamp}.txt")
    
    logging.basicConfig(filename=log_file, level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def debug(message, level="info", console_only=True):
    # ... (existing debug function code)
    
    if not console_only and level in ["warning", "error", "fail"]:
        logging.error(message)