# from gpiozero import Buzzer
from time import sleep

# bz =  None   # replace None with the correct pin number
# bz.off() 

def success():
    """3 short beeps."""
    # TODO: on/off pattern
    buzz = bz(2)
    #sets one longn buzzer that is 0.5 seconds long 
    try:
        bz.beep(on_time = .1, off_time = .1, n = 3, background = False)
    finally:
        bz.close()
    pass

def fail():
    """1 long beep."""
    # TODO: on/off pattern
     #bz.on, sleep(10, bz.off 
    buzz = bz(2)
    #sets one longn buzzer that is 0.5 seconds long 
    try:
        bz.beep(on_time = 1, off_time = 1, n = 1, background = False)
    finally:
        bz.close()
    pass

def cleanup():
    pass
    # bz.off()
    # bz.close()
