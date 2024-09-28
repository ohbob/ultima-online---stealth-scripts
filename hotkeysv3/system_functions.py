import time
from utils import debug
from functools import wraps

class SystemFunctions:
    timers = {}
    hotkeys_enabled = True

    @classmethod
    def check_and_set_timer(cls, name, duration_ms):
        now = time.time() * 1000  # Convert to milliseconds
        if name not in cls.timers or now >= cls.timers[name]:
            cls.timers[name] = now + duration_ms
            return True
        return False

    @classmethod
    def reset_timer(cls, name):
        cls.timers.pop(name, None)

    @classmethod
    def get_remaining_time(cls, name):
        if name in cls.timers:
            return max(0, cls.timers[name] - time.time() * 1000)
        return 0

    @classmethod
    def cooldown(cls, name, duration_ms):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if cls.check_and_set_timer(name, duration_ms):
                    result = func(*args, **kwargs)
                    if not result:
                        cls.reset_timer(name)  # Only reset if function fails
                    return result
                return False
            return wrapper
        return decorator

    @classmethod
    def toggle_all_hotkeys(cls):
        cls.hotkeys_enabled = not cls.hotkeys_enabled
        debug(f"Hotkeys {'enabled' if cls.hotkeys_enabled else 'disabled'}", 
              "success" if cls.hotkeys_enabled else "fail")