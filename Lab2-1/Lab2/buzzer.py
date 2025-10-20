from gpiozero import Buzzer
from time import sleep

bz = Buzzer(2)
bz.off() 

def success():
    """3 short beeps."""
    # TODO: on/off pattern
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
    #sets one longn buzzer that is 0.5 seconds long 
    try:
        bz.beep(on_time = 1, off_time = 1, n = 1, background = False)
    finally:
        bz.close()
    pass

def cleanup():
    bz.off()
    bz.close()
