import time
import board
from digitalio import DigitalInOut, Direction, Pull
import storage
import extern
from userConfig import x80_pinout
print("boot.py, X80 flag:", x80_pinout)
if x80_pinout:
    from x80PinMap import KEY_ONE, KEY_TWO, KEY_THREE, BUZZER_PIN
else:
    from userPinMap import KEY_ONE, KEY_TWO, KEY_THREE, BUZZER_PIN


#IP_NO_PULL = 0
#IP_PULLUP = 1

#MORSE_KEY_IP_TYPE = IP_NO_PULL #original

button_one_pin = DigitalInOut(KEY_ONE)
button_one_pin.direction = Direction.INPUT
if not x80_pinout:
    button_one_pin.pull = Pull.UP  # when x80 board not used

button_two_pin = DigitalInOut(KEY_TWO)
button_two_pin.direction = Direction.INPUT
button_two_pin.pull = Pull.UP

button_three_pin = DigitalInOut(KEY_THREE)
button_three_pin.direction = Direction.INPUT
button_three_pin.pull = Pull.UP

extern.buzzer_pin = DigitalInOut(BUZZER_PIN)
extern.buzzer_pin.direction = Direction.OUTPUT
extern.buzzer_set_state(False)

print("Boot")
if button_one_pin.value == False and button_two_pin.value == True and button_three_pin.value == False:    
    print("Filesystem ready for update.")
    #storage.remount("/", True)            
    extern.buzzer_set_state(True)
    time.sleep(2)
    extern.buzzer_set_state(False)
else:        
    print("Filesystem is readonly.")
    #storage.remount("/", False)    
    #print("data from file")
    #extern.readDataFromFS()
    