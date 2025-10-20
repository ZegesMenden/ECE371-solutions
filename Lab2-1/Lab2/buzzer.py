from gpiozero import Buzzer
from time import sleep

bz = Buzzer(2)   # replace None with the correct pin number
bz.off() 

def success():
    """3 short beeps."""
    # TODO: on/off pattern
    try:
        for i in range(3):
            bz.on()
            sleep(0.1)
            bz.off()
            sleep(0.1)
    except Exception as e:
        print(f"Error in success buzzer pattern: {e}")
    finally:
        cleanup()    

def fail():
    """1 long beep."""
    # TODO: on/off pattern
    try:
        bz.on()
        sleep(1.0)
        bz.off()
    except Exception as e:
        print(f"Error in fail buzzer pattern: {e}")
    finally:
        cleanup()

def cleanup():
    bz.off()
    bz.close()