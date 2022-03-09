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
from morseCode_h import *
from userPinMap import *
from morseCode import *
import extern

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

NUMPIXELS = 1       #// v0.2

# dotstart initialization
import adafruit_dotstar
pixels = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, NUMPIXELS, brightness=0.3, auto_write=False)

# neopixel initialization
#import neopixel
#pixels = neopixel.NeoPixel(board.NEOPIXEL, NUMPIXELS, brightness=0.3, auto_write=False)

BUTTON_ONE = KEY_ONE
BUTTON_TWO = KEY_TWO
BUTTON_THREE = KEY_THREE
USER_BUTTON = USER_SWITCH
USER_BUTTON2 = USER_SWITCH2
#HARD_RESET_PIN = RESET_PIN       #// v0.3g
BUZZER = BUZZER_PIN
DOT = '.'
DASH = '-'

t1 = 0 
t2 = 0
currentMillis = 0
deviceBleName = DEVICE_BLE_NAME
deviceBleName2 = DEVICE_BLE_NAME2     #// v0.3c
deviceManuf = DEVICE_MANUFACTURER
deviceModelName = DEVICE_MODEL_NAME

codeStrIndex = 0


keyscan = 0
lastCentral_name = ""
flag_manualDisconnection = 0
manualDisconnTicks = 0


lastMouseMovTicks = 0                      #// v0.3
lastBeepTicks = 0                          #// v0.3
lastUserBtnCheckTicks = 0                  #// v0.3
lastScKeyCheckTicks = 0                    #// v0.3

maxSwapConn = MAXIMUM_SWAP_CONNECTIONS     #// v0.3c

flag_blinkNeopixel = 0                     #// v0.3c
flag_blinkOnOff = 0                        #// v0.3c

lastRepeatCmdSentTicks = 0                 #// v0.3e

last_callback_time = 0

if TWO_BUTTON_MODE or THREE_BUTTON_MODE:  #// v0.3
    flag_fastTypingMode = FAST_TYPING_MODE
else:
    flag_fastTypingMode = 0

if FAST_TYPING_MODE:                                     #// v0.3
    charLength = (DOT_LENGTH * 3) + 250
else:
    charLength = (DOT_LENGTH * 3) + 100

def loop():
    global flag_manualDisconnection, currentMillis, flag_switchControlMode, lastScKeyCheckTicks, manualDisconnTicks, lastCentral_name, currSwapConnIndex, flag_repeatCmdEnable, lastRepeatCmdSentTicks
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
            if ONE_BUTTON_MODE:
                checkButton(extern.button_one_pin)  
            if TWO_BUTTON_MODE:
                checkButton(extern.button_one_pin)
                checkButton(extern.button_two_pin) 
            if THREE_BUTTON_MODE:
                checkButton(extern.button_one_pin)
                checkButton(extern.button_two_pin)
                checkButtonThreeForEndChar()

        if flag_manualDisconnection:  
            if currentMillis - manualDisconnTicks >= LAST_CONNECTION_CHECK_TIMEOUT:    
                lastCentral_name = ""
                flag_manualDisconnection = 0
                extern.currSwapConnIndex = 0              #// v0.3c
                #// Write updated data into FS
                extern.writeDataToFS()                              #// v0.3e
        
        if extern.flag_repeatCmdEnable:                #// v0.3e  
            if currentMillis - lastRepeatCmdSentTicks >= INTERVAL_SEND_REPEAT_CMD:
                lastRepeatCmdSentTicks = currentMillis
                handleRepeatCmdAction()

        checkForConnectionSwap()

def checkButton(button_pin):
    global button_one_pin, button_two_pin, button_three_pin, DOT, DASH, t1, t2, codeStr, codeStrIndex, signal_len, flag_fastTypingMode, charLength, lastBeepTicks    
    #JUMP:
    while True:
        check_timer_callback()
        #print(button_pin.value)
        if button_pin.value == False:    
            if flag_fastTypingMode:           #// v0.3    
                t1 = millis()
                lastBeepTicks = t1      
                while button_pin.value == False:
                    check_timer_callback()
                    if millis() - lastBeepTicks >= DOT_LENGTH:                    
                        lastBeepTicks = millis()
                        extern.buzzer_set_state(True)#BUZZER_ON;                            #// v0.3f
                        if button_pin == extern.button_one_pin:                            
                            extern.codeStr += DOT
                            codeStrIndex+=1
                        else:                                                    
                            extern.codeStr += DASH
                            codeStrIndex+=1
                        time.sleep(0.05)          
                        extern.buzzer_set_state(False)#BUZZER_OFF;                            #// v0.3f          
            else:    
                t1 = millis()
                extern.buzzer_set_state(True)#BUZZER_ON;                                 #// v0.3f                
                while (button_pin.value == False and (millis() - t1) < 2000):
                    pass
                t2 = millis()
                extern.buzzer_set_state(False)#BUZZER_OFF;                                #// v0.3f

                extern.signal_len = t2 - t1
                if(extern.signal_len > 50):            
                    if ONE_BUTTON_MODE:                        
                        extern.codeStr += findDotOrDash();               #//function to read dot or dash             
                        print(extern.codeStr)
                        codeStrIndex+=1
                    
                    if TWO_BUTTON_MODE or THREE_BUTTON_MODE:
                        if button_pin == extern.button_one_pin:                                             
                            extern.codeStr += DOT     #// v0.2
                            codeStrIndex+=1                
                        elif button_pin == extern.button_two_pin:
                            
                            extern.codeStr += DASH    #// v0.2           
                            codeStrIndex+=1

        if ONE_BUTTON_MODE:
            #print("continue: ",(millis() - t2) < charLength, codeStrIndex < MORSE_CODE_MAX_LENGTH)
            #print("char length: ", charLength)                    
            continue_flag = False
            while (millis() - t2) < charLength and codeStrIndex < MORSE_CODE_MAX_LENGTH:                
                if button_pin.value == False:                        
                    continue_flag = True
                    break                    
            if continue_flag:
                continue
        break
        
    if TWO_BUTTON_MODE:        #// v0.3
        if not flag_fastTypingMode:
            if (millis() - t2) >= charLength or codeStrIndex >= MORSE_CODE_MAX_LENGTH:
                if codeStrIndex >= 1:
                    convertor()
                    codeStrIndex = 0        
        else:
            if (millis() - lastBeepTicks) >= charLength or codeStrIndex >= MORSE_CODE_MAX_LENGTH:
                if codeStrIndex >= 1:
                    convertor()
                    codeStrIndex = 0

    #ifdef THREE_BUTTON_MODE
    #endif

    if ONE_BUTTON_MODE:
        if codeStrIndex >= 1:                    
            convertor()
            codeStrIndex = 0        
        else:
            pass

    #ifdef TWO_BUTTON_MODE
    #endif

def checkButtonThreeForEndChar():
    global button_three_pin, codeStrIndex

    if codeStrIndex >= 1 and extern.button_three_pin.value == False:
        extern.buzzer_set_state(True)#BUZZER_ON;                            #// v0.3f
        convertor()
        codeStrIndex = 0
        extern.buzzer_set_state(False)#BUZZER_OFF;                           #// v0.3f
    else:
        pass

def checkForConnectionSwap():
    return # temp
    global user_button_pin, user_button2_pin, reset_pin, currentMillis, keyscan, lastUserBtnCheckTicks, flag_switchControlMode, currMode
    
    if currentMillis - lastUserBtnCheckTicks >= 100:
        lastUserBtnCheckTicks = currentMillis
        if user_button_pin.value == False:
            if keyscan:       #// v0.3b      
                keyscan = 0
                if SERIAL_DEBUG_EN:
                    print("Connection Swap Switch Pressed");                
                handleBleConnectionSwap()     #// v0.3        
        elif user_button2_pin.value == False:       #// v0.3b    
            if(keyscan):        
                #//uint16_t connectionHandle = 0;
                #//BLEConnection* connection = NULL;
                
                keyscan = 0
                """
                /*
                // v0.3c
                Bluefruit.Advertising.stop();
                Bluefruit.Advertising.clearData();
                Bluefruit.ScanResponse.clearData();
                connectionHandle = Bluefruit.connHandle();                
                connection = Bluefruit.Connection(connectionHandle);        
                delay(1000);
                connection->disconnect();
                delay(2000);
                // v0.3c
                */
                // v0.3g
                // Hard Reset
                
                // Before reseting MCU, Do not disconnect BLE
                // Change Switch control/Morse mode variables
                // Write into FS

                // Then Reset MCU
                
                // After Reset
                // Read FS - Update variables
                // Take MAC & BLE advt. name accordingly
                // Start Advt.
                
                
                // v0.3g
                """
                if not extern.flag_switchControlMode:        
                    extern.flag_switchControlMode = 1
                    currMode = SW_CTRL_MODE              #// v0.3e  
                    if SERIAL_DEBUG_EN:
                        print("Switch Control Mode Enable")
                else:        
                    extern.flag_switchControlMode = 0
                    currMode = MORSE_MODE               #// v0.3e
                    if SERIAL_DEBUG_EN:
                        print("Switch Control Mode Disable")
                #// Write updated data into FS
                extern.writeDataToFS()                        #// v0.3e

                #// v0.3g
                if SERIAL_DEBUG_EN:
                    print("Reseting MCU")
                    time.sleep(2)        
                
                reset_pin.value = False
                #// v0.3g    
    else:      #// v0.3b          
        keyscan = 1    

def bleConnectCallback():       #// v0.3c
    global ble, lastCentral_name, flag_manualDisconnection, maxSwapConn, currSwapConnIndex, swapConnDeviceNames, flag_blinkNeopixel
    i = 0 #local
    connectionHandle = 0 #local
    connection = None #local
    central_name = "" #local
    peer_connection = ble.connections[0]
    central_name = getCentralName(peer_connection)

    if SERIAL_DEBUG_EN:
        print("Connection Req from ")
        print(central_name)

    if(flag_manualDisconnection):        
        for i in range(maxSwapConn):        
            if central_name == extern.swapConnDeviceNames[i]:            
                if SERIAL_DEBUG_EN:
                    print("Name matched in last list, Disconnecting...")                
                
                setNeopixelColor(0, 0, 0)      #// Off      #// v0.3c
                peer_connection.disconnect()

                break

    if i == maxSwapConn or (not flag_manualDisconnection):    
        if SERIAL_DEBUG_EN:
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
    if currMode == SW_CTRL_MODE:
        new_mac[5] = 0xDD

    _bleio.adapter.address = _bleio.Address(new_mac, _bleio.Address.RANDOM_STATIC)

    mac =_bleio.adapter.address.address_bytes

    print("New mac address: ")
    for byte in mac:    
        print(hex(byte))

def handleBleConnectionSwap():      #// v0.3
    return #temp
    global ble, currSwapConnIndex, maxSwapConn, flag_manualDisconnection, manualDisconnTicks, swapConnDeviceNames, flag_blinkNeopixel
    
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
    if SERIAL_DEBUG_EN:
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
    global currSwapConnIndex, flag_blinkNeopixel, flag_blinkNeopixel
    if flag_blinkNeopixel:

        if flag_blinkOnOff:    
            flag_blinkOnOff = 0
            setNeopixelColor(0, 0, 0)      #// Off
        else:    
            flag_blinkOnOff = 1
            setNeopixelIndication(extern.currSwapConnIndex)


### SETUP ###
if ONE_BUTTON_MODE: 
    extern.button_one_pin = DigitalInOut(BUTTON_ONE)
    extern.button_one_pin.direction = Direction.INPUT

if TWO_BUTTON_MODE:        
    extern.button_one_pin = DigitalInOut(BUTTON_ONE)
    extern.button_one_pin.direction = Direction.INPUT
    
    extern.button_two_pin = DigitalInOut(BUTTON_TWO)
    extern.button_two_pin.direction = Direction.INPUT
    extern.button_two_pin.pull = Pull.UP

if THREE_BUTTON_MODE:
        extern.button_one_pin = DigitalInOut(BUTTON_ONE)
        extern.button_one_pin.direction = Direction.INPUT
        
        extern.button_two_pin = DigitalInOut(BUTTON_TWO)
        extern.button_two_pin.direction = Direction.INPUT
        extern.button_two_pin.pull = Pull.UP

        extern.button_three_pin = DigitalInOut(BUTTON_THREE)
        extern.button_three_pin.direction = Direction.INPUT
        extern.button_three_pin.pull = Pull.UP

user_button_pin = DigitalInOut(USER_BUTTON)
user_button_pin.direction = Direction.INPUT
user_button_pin.pull = Pull.UP

user_button2_pin = DigitalInOut(USER_BUTTON2)
user_button2_pin.direction = Direction.INPUT
user_button2_pin.pull = Pull.UP

extern.buzzer_pin = DigitalInOut(BUZZER)
extern.buzzer_pin.direction = Direction.OUTPUT
extern.buzzer_set_state(False)                                   #// v0.3f

#reset_pin = DigitalInOut(HARD_RESET_PIN)
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

if(extern.currMode == MORSE_MODE):                     #// v0.3g    
    ble.name  = deviceBleName
    scan_response.complete_name = deviceBleName
else:    
    ble.name  = deviceBleName2
    scan_response.complete_name = deviceBleName2

loop()