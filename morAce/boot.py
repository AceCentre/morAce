import time
import board
from digitalio import DigitalInOut, Direction, Pull
import storage
import extern
from user.config import x80_pinout, buzzer_freq, sound_level, saving_parameters
import supervisor
import pwmio

supervisor.disable_ble_workflow()

if x80_pinout:
    from x80PinMap import button_one_pin, button_two_pin, button_three_pin, buzzer_pin
else:
    from user.userPinMap import button_one_pin, button_two_pin, button_three_pin, buzzer_pin


#IP_NO_PULL = 0
#IP_PULLUP = 1

#MORSE_KEY_IP_TYPE = IP_NO_PULL #original

button_one = DigitalInOut(button_one_pin)
button_one.direction = Direction.INPUT
if not x80_pinout:
    button_one.pull = Pull.UP  # when x80 board not used

button_two = DigitalInOut(button_two_pin)
button_two.direction = Direction.INPUT
button_two.pull = Pull.UP

button_three = DigitalInOut(button_three_pin)
button_three.direction = Direction.INPUT
button_three.pull = Pull.UP

extern.buzzer = pwmio.PWMOut(buzzer_pin, duty_cycle=0, frequency=buzzer_freq, variable_frequency=True)

# calculating buzzer pwm
max_buzzer_pwm = 4095
sound_levels_n = 10
if sound_level > sound_levels_n:
    sound_level = sound_levels_n
elif sound_level < 0:
    sound_level = 0

extern.buzzer_duty_cycle = int(sound_level * (max_buzzer_pwm/sound_levels_n))

print("Boot")
if saving_parameters:
    if button_one.value == False:
        print("Filesystem ready for update.")
        storage.remount("/", True)
        extern.buzzer_activate(buzzer_freq)
        time.sleep(2)
        extern.buzzer_deactivate()
    else:
        print("Filesystem is readonly.")
        storage.remount("/", False)
        print("data from file")
        extern.readDataFromFS()
        