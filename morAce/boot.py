"""
import time
import board
from digitalio import DigitalInOut, Direction, Pull
import storage
from userPinMap import KEY_ONE, KEY_TWO, KEY_THREE, BUZZER_PIN
import extern

IP_NO_PULL = 0
IP_PULLUP = 1

MORSE_KEY_IP_TYPE = IP_NO_PULL #original

button_one_pin = DigitalInOut(KEY_ONE)
button_one_pin.direction = Direction.INPUT
button_two_pin = DigitalInOut(KEY_TWO)
button_two_pin.direction = Direction.INPUT
button_three_pin = DigitalInOut(KEY_THREE)
button_three_pin.direction = Direction.INPUT

extern.buzzer_pin = DigitalInOut(BUZZER_PIN)
extern.buzzer_pin.direction = Direction.OUTPUT
extern.buzzer_set_state(False)

if MORSE_KEY_IP_TYPE != IP_NO_PULL:     #// v0.3f    
    button_one_pin.pull = Pull.UP
    button_two_pin.pull = Pull.UP
    button_three_pin.pull = Pull.UP
print("Boot")
if button_one_pin.value == False and button_two_pin.value == True and button_three_pin.value == False:    
    print("Ready for update")
    storage.remount("/", True)            
    extern.buzzer_set_state(True)
    time.sleep(2)
    extern.buzzer_set_state(False)
else:        
    storage.remount("/", False)
    print("data from file")
    extern.readDataFromFS()
"""
    
        


