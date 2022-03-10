import time
import supervisor
import board
from digitalio import DigitalInOut, Direction, Pull

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

_TICKS_PERIOD = const(1<<29)
_TICKS_MAX = const(_TICKS_PERIOD-1)
_TICKS_HALFPERIOD = const(_TICKS_PERIOD//2)

def ticks_add(ticks, delta):
    "Add a delta to a base number of ticks, performing wraparound at 2**29ms."
    return (ticks + delta) % _TICKS_PERIOD

def ticks_diff(ticks1, ticks2):
    "Compute the signed difference between two ticks values, assuming that they are within 2**28 ticks"
    diff = (ticks1 - ticks2) & _TICKS_MAX
    diff = ((diff + _TICKS_HALFPERIOD) & _TICKS_MAX) - _TICKS_HALFPERIOD
    return diff

def ticks_less(ticks1, ticks2):
    "Return true iff ticks1 is less than ticks2, assuming that they are within 2**28 ticks"
    return ticks_diff(ticks1, ticks2) < 0

time_var = 0
prev_tick = supervisor.ticks_ms()
def millis():
    global time_var, prev_tick
    curr_tick = supervisor.ticks_ms()
    time_var += ticks_diff(curr_tick,prev_tick)
    prev_tick=curr_tick
    return time_var

#IP_NO_PULL = 0
#IP_PULLUP = 1

#MORSE_KEY_IP_TYPE = IP_NO_PULL #original

# dotstart initialization
import adafruit_dotstar
pixels = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.3, auto_write=False)

# neopixel initialization
#import neopixel
#pixels = neopixel.NeoPixel(neopixel_pin, 1, brightness=0.3, auto_write=False)

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
flag_manualDisconnection = 0
manualDisconnTicks = 0

lastMouseMovTicks = 0                      #// v0.3
lastBeepTicks = 0                          #// v0.3
lastUserBtnCheckTicks = 0                  #// v0.3
lastScKeyCheckTicks = 0                    #// v0.3

flag_blinkNeopixel = 0                     #// v0.3c
flag_blinkOnOff = 0                        #// v0.3c

lastRepeatCmdSentTicks = 0                 #// v0.3e

last_callback_time = 0

if two_button_mode or three_button_mode:  #// v0.3
    flag_fastTypingMode = fast_typing_mode
else:
    flag_fastTypingMode = 0

if fast_typing_mode:                                     #// v0.3
    charLength = (dot_length * 3) + 250
else:
    charLength = (dot_length * 3) + 100

def loop():
    global flag_manualDisconnection, currentMillis, lastScKeyCheckTicks, manualDisconnTicks, lastCentral_name, lastRepeatCmdSentTicks
    global ble, advertisement, scan_response    
    while True:        
        if not ble.connected:
            ble.start_advertising(advertisement, scan_response)
            print("No connection")
            while not ble.connected:
                print("waiting for connection")
                time.sleep(1)
            print("Connection made")
            bleConnectCallback()              # calling callback after connection made
        currentMillis = millis()        
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

        if flag_manualDisconnection:  
            if currentMillis - manualDisconnTicks >= last_connection_check_timeout:    
                lastCentral_name = ""
                flag_manualDisconnection = 0
                extern.currSwapConnIndex = 0              #// v0.3c
                #// Write updated data into FS
                extern.writeDataToFS()                              #// v0.3e
        
        if extern.flag_repeatCmdEnable:                #// v0.3e  
            if currentMillis - lastRepeatCmdSentTicks >= interval_send_repeat_cmd:
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
                t1 = millis()
                lastBeepTicks = t1      
                while button_pin.value == False:
                    check_timer_callback()
                    if millis() - lastBeepTicks >= dot_length:                    
                        lastBeepTicks = millis()
                        extern.buzzer_set_state(True)                            #// v0.3f
                        if button_pin == extern.button_one:                            
                            extern.codeStr += dot
                            codeStrIndex+=1
                        else:                                                    
                            extern.codeStr += dash
                            codeStrIndex+=1
                        time.sleep(0.05)          
                        extern.buzzer_set_state(False)                            #// v0.3f          
            else:    
                t1 = millis()
                extern.buzzer_set_state(True)                                 #// v0.3f                
                while (button_pin.value == False and (millis() - t1) < 2000):
                    pass
                t2 = millis()
                extern.buzzer_set_state(False)                                #// v0.3f

                extern.signal_len = t2 - t1
                if(extern.signal_len > 50):            
                    if one_button_mode:                        
                        extern.codeStr += findDotOrDash();               #//function to read dot or dash                        
                        codeStrIndex+=1
                    
                    if two_button_mode or three_button_mode:
                        if button_pin == extern.button_one:                                             
                            extern.codeStr += dot     #// v0.2
                            codeStrIndex+=1                
                        elif button_pin == extern.button_two:
                            
                            extern.codeStr += dash    #// v0.2           
                            codeStrIndex+=1

        if one_button_mode:            
            continue_flag = False
            while (millis() - t2) < charLength and codeStrIndex < morse_code_max_length:                
                if button_pin.value == False:                        
                    continue_flag = True
                    break                    
            if continue_flag:
                continue
        break
        
    if two_button_mode:        #// v0.3
        if not flag_fastTypingMode:
            if (millis() - t2) >= charLength or codeStrIndex >= morse_code_max_length:
                if codeStrIndex >= 1:
                    convertor()
                    codeStrIndex = 0        
        else:
            if (millis() - lastBeepTicks) >= charLength or codeStrIndex >= morse_code_max_length:
                if codeStrIndex >= 1:
                    convertor()
                    codeStrIndex = 0

    #ifdef THREE_BUTTON_MODE
    #endif

    if one_button_mode:
        if codeStrIndex >= 1:                    
            convertor()
            codeStrIndex = 0        
        else:
            pass

    #ifdef TWO_BUTTON_MODE
    #endif

def checkButtonThreeForEndChar():
    global codeStrIndex

    if codeStrIndex >= 1 and extern.button_three.value == False:
        extern.buzzer_set_state(True)                            #// v0.3f
        convertor()
        codeStrIndex = 0
        extern.buzzer_set_state(False)                           #// v0.3f
    else:
        pass

def checkForConnectionSwap():
    return # temp
    global user_button, user_button2, reset_pin, currentMillis, keyscan, lastUserBtnCheckTicks, currMode
    
    if currentMillis - lastUserBtnCheckTicks >= 100:
        lastUserBtnCheckTicks = currentMillis
        if user_button.value == False:
            if keyscan:       #// v0.3b      
                keyscan = 0
                if serial_debug_en:
                    print("Connection Swap Switch Pressed");                
                handleBleConnectionSwap()     #// v0.3        
        elif user_button2.value == False:       #// v0.3b    
            if(keyscan):        
                #//uint16_t connectionHandle = 0;
                #//BLEConnection* connection = NULL;
                
                keyscan = 0

                if not extern.flag_switchControlMode:        
                    extern.flag_switchControlMode = 1
                    currMode = sw_ctrl_mode              #// v0.3e  
                    if serial_debug_en:
                        print("Switch Control Mode Enable")
                else:        
                    extern.flag_switchControlMode = 0
                    currMode = morse_mode               #// v0.3e
                    if serial_debug_en:
                        print("Switch Control Mode Disable")
                #// Write updated data into FS
                extern.writeDataToFS()                        #// v0.3e

                #// v0.3g
                if serial_debug_en:
                    print("Reseting MCU")
                    time.sleep(2)        
                
                reset_pin.value = False
                #// v0.3g    
    else:      #// v0.3b          
        keyscan = 1    

def bleConnectCallback():       #// v0.3c
    global ble, lastCentral_name, flag_manualDisconnection, maxSwapConn, flag_blinkNeopixel
    i = 0 #local
    connectionHandle = 0 #local
    connection = None #local
    central_name = "" #local
    peer_connection = ble.connections[0]
    central_name = getCentralName(peer_connection)

    if serial_debug_en:
        print("Connection Req from ")
        print(central_name)

    if(flag_manualDisconnection):        
        for i in range(maxSwapConn):        
            if central_name == extern.swapConnDeviceNames[i]:            
                if serial_debug_en:
                    print("Name matched in last list, Disconnecting...")                
                
                setNeopixelColor(0, 0, 0)      #// Off      #// v0.3c
                peer_connection.disconnect()

                break

    if i == maxSwapConn or (not flag_manualDisconnection):    
        if serial_debug_en:
            print("New Connection: ", central_name)

        #// v0.3c
        flag_blinkNeopixel = 0
        setNeopixelIndication(extern.currSwapConnIndex)
        lastCentral_name = ""
        extern.swapConnDeviceNames[extern.currSwapConnIndex] = ""
        extern.swapConnDeviceNames[extern.currSwapConnIndex+1] = ""
        extern.swapConnDeviceNames[extern.currSwapConnIndex] = central_name
        lastCentral_name = central_name
        #// v0.3c

        #// Write updated data into FS
        extern.writeDataToFS()                              #// v0.3e
            
        flag_manualDisconnection = 0      

def getCentralName(connection):    
    device_services = connection._bleio_connection.discover_remote_services()
    for service in device_services:
        if service.uuid == _bleio.UUID(0x1800):
            for characteristic in service.characteristics:
                if characteristic.uuid == _bleio.UUID(0x2A00):
                    return characteristic.value.decode('utf-8')


def setNeopixelColor(r, g, b):    #// v0.2
    global pixels
    pixels.fill((0,0,0))
    pixels[0] = (r, g, b)
    pixels.show()

def setNeopixelIndication(index):           #// v0.3c
    if index == 0:    
        setNeopixelColor(0, 0, 255);        #// Blue        
    elif index == 1:
        setNeopixelColor(0, 255, 255);      #// Cyan    
    elif index == 2:
        setNeopixelColor(0, 255, 0);        #// Green
    elif index == 3:    
        setNeopixelColor(255, 255, 0);      #// Yellow    
    elif index == 4:    
        setNeopixelColor(255, 128, 0);      #// Orange



def changeMacAddress():                           #// v0.3g
    return # temp
    global currMode
    mac = bytearray(_bleio.adapter.address.address_bytes)
    print("Current mac address: ")
    for byte in mac:    
        print(hex(byte))

    new_mac = mac
    if currMode == sw_ctrl_mode:
        new_mac[5] = 0xDD

    _bleio.adapter.address = _bleio.Address(new_mac, _bleio.Address.RANDOM_STATIC)

    mac =_bleio.adapter.address.address_bytes

    print("New mac address: ")
    for byte in mac:    
        print(hex(byte))

def handleBleConnectionSwap():      #// v0.3
    return #temp
    global ble, maxSwapConn, flag_manualDisconnection, manualDisconnTicks, flag_blinkNeopixel
    
    connection = ble.connections[0]

    #// v0.3c
    extern.currSwapConnIndex+=1
    if extern.currSwapConnIndex >= maxSwapConn:    
        extern.currSwapConnIndex = 0
    
    extern.swapConnDeviceNames[extern.currSwapConnIndex] = ""
    #// v0.3c

    #// Write updated data into FS
    extern.writeDataToFS()                              #// v0.3e

    time.sleep(2)
    connection.disconnect()
    if serial_debug_en:
        print("Disconnected")

    setNeopixelColor(0, 0, 0)      #// Off      #// v0.3c
    flag_blinkNeopixel = 1                   #// v0.3c 

    flag_manualDisconnection = 1
    manualDisconnTicks = millis()

# soft timer imitation
def check_timer_callback():
    global last_callback_time    
    
    if (millis() - last_callback_time) > 500:        
        softTimer_callback()
        last_callback_time = millis()

def softTimer_callback():       #// v0.3c
    global flag_blinkNeopixel, flag_blinkNeopixel
    if flag_blinkNeopixel:

        if flag_blinkOnOff:    
            flag_blinkOnOff = 0
            setNeopixelColor(0, 0, 0)      #// Off
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

user_button = DigitalInOut(user_switch)
user_button.direction = Direction.INPUT
user_button.pull = Pull.UP

user_button2 = DigitalInOut(user_switch2)
user_button2.direction = Direction.INPUT
user_button2.pull = Pull.UP

extern.buzzer = DigitalInOut(buzzer_pin)
extern.buzzer.direction = Direction.OUTPUT
extern.buzzer_set_state(False)                                   #// v0.3f

#reset_pin = DigitalInOut(hard_reset_pin)
#reset_pin.direction = Direction.OUTPUT
#reset_pin.value = True

#// Set Neopixel Colour
setNeopixelColor(0, 0, 0)   

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

ble = adafruit_ble.BLERadio()

#// Set Device MAC Address
#changeMacAddress()

if(extern.currMode == morse_mode):                     #// v0.3g    
    ble.name  = deviceBleName
    scan_response.complete_name = deviceBleName
else:    
    ble.name  = deviceBleName2
    scan_response.complete_name = deviceBleName2

loop()