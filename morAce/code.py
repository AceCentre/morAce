import time

import microcontroller
import board
from digitalio import DigitalInOut, Direction, Pull
import pwmio

from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

import _bleio
import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService

from userConfig import *
from morseCode import *
import extern

if x80_pinout:
    from x80PinMap import *
else:
    from userPinMap import *

#IP_NO_PULL = 0
#IP_PULLUP = 1

#MORSE_KEY_IP_TYPE = IP_NO_PULL #original

# dotstart initialization
import adafruit_dotstar
extern.pixels = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.3, auto_write=False)

# neopixel initialization
#import neopixel
#extern.pixels = neopixel.NeoPixel(neopixel_pin, 1, brightness=0.3, auto_write=False)

t1 = 0
t2 = 0
currentMillis = 0
deviceBleName = device_ble_name
deviceBleName2 = device_ble_name2     #// v0.3c
deviceManuf = device_manufacturer
deviceModelName = device_model_name

codeStrIndex = 0

keyscan = 0
lastCentral_name = ""

lastMouseMovTicks = 0                      #// v0.3
lastBeepTicks = 0                          #// v0.3
lastUserBtnCheckTicks = 0                  #// v0.3
lastScKeyCheckTicks = 0                    #// v0.3

flag_blinkOnOff = 0                        #// v0.3c

lastRepeatCmdSentTicks = 0                 #// v0.3e

last_callback_time = 0

if two_button_mode or three_button_mode:  #// v0.3
    flag_fastTypingMode = fast_typing_mode
else:
    flag_fastTypingMode = 0

charLength = (
    (dot_length * 3) + 250 if fast_typing_mode else (dot_length * 3) + 100
)

def loop():
    global currentMillis, lastScKeyCheckTicks, lastCentral_name, lastRepeatCmdSentTicks
    global advertisement, scan_response
    while True:
        if not extern.ble.connected:
            extern.ble.start_advertising(advertisement, scan_response)
            print("No connection")
            while not extern.ble.connected:
                print("waiting for connection")
                time.sleep(1)
            print("Connection made")
            bleConnectCallback()              # calling callback after connection made
        currentMillis = extern.millis()
        if extern.flag_switchControlMode:
            if currentMillis - lastScKeyCheckTicks >= 100:
                lastScKeyCheckTicks = currentMillis
                handleSwitchControlKeypress()
        else:
            if one_button_mode:
                checkButton(extern.button_one)
            if two_button_mode:
                checkButton(extern.button_one)
                checkButton(extern.button_two)
            if three_button_mode:
                checkButton(extern.button_one)
                checkButton(extern.button_two)
                checkButtonThreeForEndChar()

        if (
            extern.flag_manualDisconnection
            and currentMillis - extern.manualDisconnTicks
            >= last_connection_check_timeout
        ):
            lastCentral_name = ""
            extern.flag_manualDisconnection = 0
            extern.currSwapConnIndex = 0              #// v0.3c
            #// Write updated data into FS
            extern.writeDataToFS()                              #// v0.3e

        if (
            extern.flag_repeatCmdEnable
            and currentMillis - lastRepeatCmdSentTicks
            >= interval_send_repeat_cmd
        ):
            lastRepeatCmdSentTicks = currentMillis
            handleRepeatCmdAction()

        checkForConnectionSwap()

def checkButton(button_pin):
    global dot, dash, t1, t2, codeStrIndex, flag_fastTypingMode, charLength, lastBeepTicks
    #JUMP:
    while True:
        check_timer_callback()
        if button_pin.value == False:
            if flag_fastTypingMode:           #// v0.3
                t1 = extern.millis()
                lastBeepTicks = t1
                while button_pin.value == False:
                    check_timer_callback()
                    if extern.millis() - lastBeepTicks >= dot_length:
                        lastBeepTicks = extern.millis()
                        extern.buzzer_activate(buzzer_freq)                            #// v0.3f
                        extern.codeStr += dot if button_pin == extern.button_one else dash
                        codeStrIndex+=1
                        time.sleep(0.05)
                        extern.buzzer_deactivate()                            #// v0.3f
            else:
                t1 = extern.millis()
                extern.buzzer_activate(buzzer_freq)                                 #// v0.3f
                while (button_pin.value == False and (extern.millis() - t1) < 2000):
                    pass
                t2 = extern.millis()
                extern.buzzer_deactivate()                                #// v0.3f

                extern.signal_len = t2 - t1
                if (extern.signal_len > 50):
                    if one_button_mode:
                        extern.codeStr += findDotOrDash();               #//function to read dot or dash
                        codeStrIndex+=1

                    if button_pin == extern.button_one:
                        if two_button_mode or three_button_mode:
                            extern.codeStr += dot     #// v0.2
                            codeStrIndex+=1
                    elif button_pin == extern.button_two:
                        if two_button_mode or three_button_mode:

                            extern.codeStr += dash    #// v0.2
                            codeStrIndex+=1

        if one_button_mode:
            continue_flag = False
            while (extern.millis() - t2) < charLength and codeStrIndex < morse_code_max_length:
                if button_pin.value == False:
                    continue_flag = True
                    break
            if continue_flag:
                continue
        break

    if two_button_mode:#// v0.3
        if flag_fastTypingMode:
            if (
                (extern.millis() - lastBeepTicks) >= charLength
                or codeStrIndex >= morse_code_max_length
            ) and codeStrIndex >= 1:
                convertor()
                codeStrIndex = 0

        elif (
            (extern.millis() - t2) >= charLength
            or codeStrIndex >= morse_code_max_length
        ) and codeStrIndex >= 1:
            convertor()
            codeStrIndex = 0
    #ifdef THREE_BUTTON_MODE
    #endif

    if one_button_mode and codeStrIndex >= 1:
        convertor()
        codeStrIndex = 0

    #ifdef TWO_BUTTON_MODE
    #endif

def checkButtonThreeForEndChar():
    global codeStrIndex

    if codeStrIndex >= 1 and extern.button_three.value == False:
        extern.buzzer_activate(buzzer_freq)                            #// v0.3f
        convertor()
        codeStrIndex = 0
        extern.buzzer_deactivate()                           #// v0.3f

def checkForConnectionSwap():
    global user_button2, currentMillis, keyscan, lastUserBtnCheckTicks

    if currentMillis - lastUserBtnCheckTicks >= 100:
        lastUserBtnCheckTicks = currentMillis
        if user_button2.value == False and keyscan:
            #//uint16_t connectionHandle = 0;
            #//BLEConnection* connection = NULL;

            keyscan = 0

            if not extern.flag_switchControlMode:
                extern.flag_switchControlMode = 1
                extern.currMode = sw_ctrl_mode              #// v0.3e
                if serial_debug_en:
                    print("Switch Control Mode Enable")
            else:
                extern.flag_switchControlMode = 0
                extern.currMode = morse_mode               #// v0.3e
                if serial_debug_en:
                    print("Switch Control Mode Disable")
            #// Write updated data into FS
            extern.writeDataToFS()                        #// v0.3e

            #// v0.3g
            if serial_debug_en:
                print("Reseting MCU")
                time.sleep(2)

            microcontroller.reset()
    else:      #// v0.3b
        keyscan = 1

def bleConnectCallback():       #// v0.3c
    global lastCentral_name, maxSwapConn
    i = 0 #local
    connectionHandle = 0 #local
    connection = None #local
    central_name = "" #local
    peer_connection = extern.ble.connections[0]

    if not peer_connection.connected:
        return

    central_name = getCentralName(peer_connection)

    if serial_debug_en:
        print("Connection Req from ")
        print(central_name)

    if(extern.flag_manualDisconnection):
        while i < maxSwapConn:
            if central_name == extern.swapConnDeviceNames[i]:
                if serial_debug_en:
                    print("Name matched in last list, Disconnecting...")

                extern.setNeopixelColor(0, 0, 0)      #// Off      #// v0.3c
                peer_connection.disconnect()

                break

            i+=1

    if i == maxSwapConn or (not extern.flag_manualDisconnection):
        if serial_debug_en:
            print("New Connection: ", central_name)

        #// v0.3c
        extern.flag_blinkNeopixel = 0
        setNeopixelIndication(extern.currSwapConnIndex)
        lastCentral_name = ""
        extern.swapConnDeviceNames[extern.currSwapConnIndex] = ""
        extern.swapConnDeviceNames[extern.currSwapConnIndex+1] = ""
        extern.swapConnDeviceNames[extern.currSwapConnIndex] = central_name
        lastCentral_name = central_name
        #// v0.3c

        #// Write updated data into FS
        extern.writeDataToFS()                              #// v0.3e

        extern.flag_manualDisconnection = 0

def getCentralName(connection):
    device_services = connection._bleio_connection.discover_remote_services()
    for service in device_services:
        if service.uuid == _bleio.UUID(0x1800):
            for characteristic in service.characteristics:
                if characteristic.uuid == _bleio.UUID(0x2A00):
                    return characteristic.value.decode('utf-8')

def setNeopixelIndication(index):           #// v0.3c
    if index == 0:
        extern.setNeopixelColor(0, 0, 255);        #// Blue
    elif index == 1:
        extern.setNeopixelColor(0, 255, 255);      #// Cyan
    elif index == 2:
        extern.setNeopixelColor(0, 255, 0);        #// Green
    elif index == 3:
        extern.setNeopixelColor(255, 255, 0);      #// Yellow
    elif index == 4:
        extern.setNeopixelColor(255, 128, 0);      #// Orange



def changeMacAddress():                           #// v0.3g
    cur_address = _bleio.adapter.address
    print("Current mac address: ", cur_address)

    new_mac = bytearray(cur_address.address_bytes)
    if extern.currMode == sw_ctrl_mode:
        new_mac[5] = 0xDD

    _bleio.adapter.address = _bleio.Address(new_mac, _bleio.Address.RANDOM_STATIC)

    new_address =_bleio.adapter.address
    print("New mac address:     ", new_address)

# soft timer imitation
def check_timer_callback():
    global last_callback_time

    if (extern.millis() - last_callback_time) > 500:
        softTimer_callback()
        last_callback_time = extern.millis()

def softTimer_callback():       #// v0.3c
    global flag_blinkOnOff
    if extern.flag_blinkNeopixel:

        if flag_blinkOnOff:
            flag_blinkOnOff = 0
            extern.setNeopixelColor(0, 0, 0)      #// Off
        else:
            flag_blinkOnOff = 1
            setNeopixelIndication(extern.currSwapConnIndex)


### SETUP ###
if one_button_mode:
    extern.button_one = DigitalInOut(button_one_pin)
    extern.button_one.direction = Direction.INPUT
    if not x80_pinout:
        extern.button_one.pull = Pull.UP  # when x80 board not used
elif two_button_mode:
    extern.button_one = DigitalInOut(button_one_pin)
    extern.button_one.direction = Direction.INPUT
    if not x80_pinout:
        extern.button_one.pull = Pull.UP  # when x80 board not used

    extern.button_two = DigitalInOut(button_two_pin)
    extern.button_two.direction = Direction.INPUT
    extern.button_two.pull = Pull.UP
elif three_button_mode:
    extern.button_one = DigitalInOut(button_one_pin)
    extern.button_one.direction = Direction.INPUT
    if not x80_pinout:
        extern.button_one.pull = Pull.UP  # when x80 board not used

    extern.button_two = DigitalInOut(button_two_pin)
    extern.button_two.direction = Direction.INPUT
    extern.button_two.pull = Pull.UP

    extern.button_three = DigitalInOut(button_three_pin)
    extern.button_three.direction = Direction.INPUT
    extern.button_three.pull = Pull.UP

user_button2 = DigitalInOut(user_switch)
user_button2.direction = Direction.INPUT
user_button2.pull = Pull.UP

extern.buzzer = pwmio.PWMOut(buzzer_pin, duty_cycle=0, frequency=buzzer_freq, variable_frequency=True)

# calculating buzzer pwm
max_buzzer_pwm = 4095
sound_levels_n = 10
if sound_level > sound_levels_n:
    sound_level = sound_levels_n
elif sound_level < 0:
    sound_level = 0

extern.buzzer_duty_cycle = int(sound_level * (max_buzzer_pwm/sound_levels_n))

#// Set Neopixel Colour
extern.setNeopixelColor(0, 0, 0)

#// Read Data from Internal File
extern.readDataFromFS()

hid = HIDService()

device_info = DeviceInfoService(software_revision=adafruit_ble.__version__,
                                manufacturer=deviceManuf,
                                model_number=deviceModelName)
advertisement = ProvideServicesAdvertisement(hid)
advertisement.appearance = 961
scan_response = Advertisement()

# setup for mouse
extern.mouse = Mouse(hid.devices)

# keyboard
extern.k = Keyboard(hid.devices)
extern.kl = KeyboardLayoutUS(extern.k)

extern.ble = adafruit_ble.BLERadio()

#// Set Device MAC Address
changeMacAddress()

if(extern.currMode == morse_mode):                     #// v0.3g
    extern.ble.name  = deviceBleName
    scan_response.complete_name = deviceBleName
else:
    extern.ble.name  = deviceBleName2
    scan_response.complete_name = deviceBleName2

loop()
