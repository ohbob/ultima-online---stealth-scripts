import time
from py_stealth import *

def field_test_normal():
    start_time = time.time()
    check_interval = 0.05  # 50ms
    total_checks = 0
    successful_actions = 0
    
    while True:
        total_checks += 1
        
        # Check for the outcome
        if CheckLag(10000):
            continue
        
        # Perform necessary actions based on the outcome
        if TargetPresent():
            action_start = time.time()
            UseSkill('Lumberjacking')
            Wait(500)
            successful_actions += 1
            action_end = time.time()
            print(f"Action completed in {action_end - action_start:.3f} seconds")
        
        # Check if we should stop the test (e.g., after a certain number of actions)
        if successful_actions >= 100:
            break
        
        # Wait for the next check
        time.sleep(check_interval)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"Field test completed:")
    print(f"Total time: {total_time:.3f} seconds")
    print(f"Total checks: {total_checks}")
    print(f"Successful actions: {successful_actions}")
    print(f"Average time per action: {total_time / successful_actions:.3f} seconds")
    print(f"Checks per second: {total_checks / total_time:.2f}")

# Call the function to run the test
field_test_normal()