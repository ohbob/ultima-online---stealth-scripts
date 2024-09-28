from utils import debug

def main(enabled=False, threshold=70):
    if enabled:
        debug(f"Auto function is enabled with threshold {threshold}", "info")
        # Add your auto function logic here
        if threshold > 50:
            debug("Threshold is greater than 50", "info")
        else:
            debug("Threshold is 50 or less", "info")
