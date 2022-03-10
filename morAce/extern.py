import userConfig

k = None        # BLE keyboard object
kl = None
mouse = None    # BLE mouse object
signal_len = 0
codeStr = ""

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

def buzzer_set_state(state):
    global buzzer
    if userConfig.buzzer_type == userConfig.active_low:
        state = not state
    
    buzzer.value = state

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
        print("Data written in DB file")

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
