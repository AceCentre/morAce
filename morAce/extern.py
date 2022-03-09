import userConfig

k = None        # BLE keyboard object
kl = None
mouse = None    # BLE mouse object
signal_len = 0
codeStr = ""

flag_mouseConMovement = 0
flag_repeatCmdEnable = 0
# new externs
currMode = userConfig.MORSE_MODE
hidMode = userConfig.DEFAULT_MODE_OF_DEVICE
mouseMoveStep = userConfig.DEFAULT_MOUSE_MOVE_STEP
swapConnDeviceNames = [""]*userConfig.MAXIMUM_SWAP_CONNECTIONS
currSwapConnIndex = 0
dbFileName = "/database.txt"

flag_switchControlMode = 0 
#
button_one_pin = None
button_two_pin = None
button_three_pin = None
buzzer_pin = None

def buzzer_set_state(state):
    global buzzer_pin
    if userConfig.BUZZER_TYPE != userConfig.ACTIVE_HIGH:
        state = not state
    
    buzzer_pin.value = state

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
    
    if userConfig.SERIAL_DEBUG_EN:
        print("Data written in DB file")

def readDataFromFS():                                #// v0.3e    
    global currMode, hidMode, mouseMoveStep, swapConnDeviceNames, currSwapConnIndex, dbFileName, flag_switchControlMode

    try:
        with open(dbFileName, "r") as dbFile:    
            if userConfig.SERIAL_DEBUG_EN:
                print("DB file open");        
            
            data_list = dbFile.read().split(",") #local
            
            if userConfig.SERIAL_DEBUG_EN:
                print(data_list)

            if len(data_list) == userConfig.MAXIMUM_SWAP_CONNECTIONS+4:        
                
                if(int(data_list[0]) == 0 or int(data_list[0]) == 1):            
                    currMode = int(data_list[0])            
                else:            
                    currMode = userConfig.MORSE_MODE          

                #// v0.3g
                if currMode == userConfig.MORSE_MODE: 
                    flag_switchControlMode = 0            
                else:            
                    flag_switchControlMode = 1;            
                #// v0.3g

                if int(data_list[1]) == 0 or int(data_list[1]) == 1:
                    hidMode = int(data_list[1])
                else:
                    hidMode = userConfig.DEFAULT_MODE_OF_DEVICE
                
                if int(data_list[2]) >= userConfig.MOUSE_SPEED_LOWER_LIMIT and int(data_list[2]) <= userConfig.MOUSE_SPEED_UPPER_LIMIT:                
                    mouseMoveStep = int(data_list[2])
                else:
                    mouseMoveStep = userConfig.DEFAULT_MOUSE_MOVE_STEP
                for i in range(userConfig.MAXIMUM_SWAP_CONNECTIONS):
                    swapConnDeviceNames[i] = data_list[i+3]                    
                
                if int(data_list[userConfig.MAXIMUM_SWAP_CONNECTIONS+3]) < userConfig.MAXIMUM_SWAP_CONNECTIONS:
                    currSwapConnIndex = int(data_list[userConfig.MAXIMUM_SWAP_CONNECTIONS+3])
                else:                
                    currSwapConnIndex = 0                

                if userConfig.SERIAL_DEBUG_EN:
                    print("-------------------------------------------")
                    print("Dev Mode:", currMode)
                    print("Morse Mode:", hidMode)
                    print("Mouse Step:", mouseMoveStep)                    
                    print("Swap names: ", swapConnDeviceNames)
                    print("Swap Index:", currSwapConnIndex)
                    print("-------------------------------------------")
            else:
                if userConfig.SERIAL_DEBUG_EN:
                    print("String is not valid")
                writeDataToFS()
    except OSError as e:
        print("Error during read. Probably file doesn't exist")
        writeDataToFS()
