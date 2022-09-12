import time
import supervisor
import user.config as userConfig

ble = None      # BLE radio object
k = None        # BLE keyboard object
kl = None
mouse = None    # BLE mouse object
pixels = None   # addressable led object
signal_len = 0
codeStr = ""

flag_manualDisconnection = 0
manualDisconnTicks = 0
flag_blinkNeopixel = 0

flag_mouseConMovement = 0
flag_repeatCmdEnable = 0
currMode = userConfig.morse_mode
hidMode = userConfig.default_mode_of_device
mouseMoveStep = userConfig.default_mouse_move_step
swapConnDeviceNames = [""]*userConfig.maxSwapConn
currSwapConnIndex = 0
dbFileName = "/database.txt"

flag_switchControlMode = 0

button_one = None
button_two = None
button_three = None

buzzer = None
buzzer_duty_cycle = 0
def buzzer_activate(freq):
    global buzzer, buzzer_duty_cycle

    buzzer.frequency = freq
    buzzer.duty_cycle = buzzer_duty_cycle

def buzzer_deactivate():
    global buzzer

    buzzer.duty_cycle = 0

def writeDataToFS():                                 #// v0.3e
    global currMode, hidMode, mouseMoveStep, swapConnDeviceNames, currSwapConnIndex, dbFileName
    buff = "" # local
    buff = buff + str(currMode) + ","
    buff = buff + str(hidMode) + ","
    buff = buff + str(mouseMoveStep) + ","
    for swapDeviceName in swapConnDeviceNames:
        buff = buff + swapDeviceName + ","
    buff = buff + str(currSwapConnIndex)
    try:
        with open(dbFileName, "w") as dbFile:
            dbFile.write(buff)
    except OSError as e:
        print("Error during write. Probably filesystem is readonly.")
        return

    if userConfig.serial_debug_en:
        print("Data written in DB file:", buff)

def readDataFromFS():                                #// v0.3e
    global currMode, hidMode, mouseMoveStep, swapConnDeviceNames, currSwapConnIndex, dbFileName, flag_switchControlMode

    try:
        with open(dbFileName, "r") as dbFile:
            if userConfig.serial_debug_en:
                print("DB file open");

            data_list = dbFile.read().split(",") #local

            if userConfig.serial_debug_en:
                print(data_list)

            if len(data_list) == userConfig.maxSwapConn+4:

                if(int(data_list[0]) == 0 or int(data_list[0]) == 1):
                    currMode = int(data_list[0])
                else:
                    currMode = userConfig.morse_mode

                #// v0.3g
                if currMode == userConfig.morse_mode:
                    flag_switchControlMode = 0
                else:
                    flag_switchControlMode = 1;
                #// v0.3g

                if int(data_list[1]) == 0 or int(data_list[1]) == 1:
                    hidMode = int(data_list[1])
                else:
                    hidMode = userConfig.default_mode_of_device

                if int(data_list[2]) >= userConfig.mouse_speed_lower_limit and int(data_list[2]) <= userConfig.mouse_speed_upper_limit:
                    mouseMoveStep = int(data_list[2])
                else:
                    mouseMoveStep = userConfig.default_mouse_move_step
                for i in range(userConfig.maxSwapConn):
                    swapConnDeviceNames[i] = data_list[i+3]

                if int(data_list[userConfig.maxSwapConn+3]) < userConfig.maxSwapConn:
                    currSwapConnIndex = int(data_list[userConfig.maxSwapConn+3])
                else:
                    currSwapConnIndex = 0

                if userConfig.serial_debug_en:
                    print("-------------------------------------------")
                    print("Dev Mode:", currMode)
                    print("Morse Mode:", hidMode)
                    print("Mouse Step:", mouseMoveStep)
                    print("Swap names: ", swapConnDeviceNames)
                    print("Swap Index:", currSwapConnIndex)
                    print("-------------------------------------------")
            else:
                if userConfig.serial_debug_en:
                    print("String is not valid")
                writeDataToFS()
    except OSError as e:
        print("Error during read. Probably file doesn't exist")
        writeDataToFS()

def handleBleConnectionSwap():      #// v0.3
    global ble, flag_manualDisconnection, manualDisconnTicks, flag_blinkNeopixel, currSwapConnIndex, swapConnDeviceNames

    connection = ble.connections[0]

    #// v0.3c
    currSwapConnIndex+=1
    if currSwapConnIndex >= userConfig.maxSwapConn:
        currSwapConnIndex = 0

    swapConnDeviceNames[currSwapConnIndex] = ""
    #// v0.3c

    #// Write updated data into FS
    writeDataToFS()                              #// v0.3e

    time.sleep(2)
    connection.disconnect()
    if userConfig.serial_debug_en:
        print("Disconnected")

    setNeopixelColor(0, 0, 0)      #// Off      #// v0.3c
    flag_blinkNeopixel = 1                   #// v0.3c

    flag_manualDisconnection = 1
    manualDisconnTicks = millis()

def setNeopixelColor(r, g, b):
    global pixels
    pixels.fill((0,0,0))
    pixels[0] = (r, g, b)
    pixels.show()

time_var = 0
prev_tick = supervisor.ticks_ms()
def millis():
    global time_var, prev_tick
    curr_tick = supervisor.ticks_ms()
    time_var += ticks_diff(curr_tick,prev_tick)
    prev_tick=curr_tick
    return time_var


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
