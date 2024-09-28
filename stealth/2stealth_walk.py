from py_stealth import *
import math

startx, starty = 2148, 3135
endx, endy = 2148, 3120

def Hide():
    if not Hidden():
        UseSkill('Hiding')
        Wait(300)

def move_step_by_step(start_x, start_y, end_x, end_y):
    dx = end_x - start_x
    dy = end_y - start_y
    distance = math.sqrt(dx**2 + dy**2)
    steps = int(distance)

    for _ in range(steps):
        Hide()
        
        # Only move if we're hidden
        if Hidden():
            step_x = start_x + int(dx * (_ + 1) / steps)
            step_y = start_y + int(dy * (_ + 1) / steps)
            NewMoveXY(step_x, step_y, False, 1, False)
        else:
            # If not hidden, wait a bit before trying to hide again
            Wait(1000)

while GetSkillValue("Stealth") < GetSkillCap("Stealth"):
    move_step_by_step(startx, starty, endx, endy)
    move_step_by_step(endx, endy, startx, starty)

