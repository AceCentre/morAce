import time

from userConfig import *
from morseCode_h import *
from userPinMap import *
import extern

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

def key_seq_press(kb_obj, key_seq):
    for keycode in key_seq:
        kb_obj._add_keycode_to_report(keycode)
        kb_obj._keyboard_device.send_report(kb_obj.report)
    kb_obj.release_all() 

BUTTON_ONE = KEY_ONE
BUTTON_TWO = KEY_TWO
BUTTON_THREE = KEY_THREE
BUZZER = BUZZER_PIN

dotLength = DOT_LENGTH
DOT = '.'
DASH = '-'
keyMouseSwitchMorseCode = MORSE_CODE_FOR_KEYB_MOUSE_SWITCH
swapBleConnectionMorseCode = MORSE_CODE_FOR_BLE_SWAP_CONNECTION   #// v0.3
repeatCmdMorseCode = MORSE_CODE_FOR_REPEAT_CMD                    #// v0.3e
mouseSpeedIncMorseCode = MORSE_CODE_FOR_MOUSE_SPEED_INC           #// v0.3e
mouseSpeedDecMorseCode = MORSE_CODE_FOR_MOUSE_SPEED_DEC           #// v0.3e
mouseSpeedSet1MorseCode = MORSE_CODE_FOR_MOUSE_SPEED_1            #// v0.3e
mouseSpeedSet5MorseCode = MORSE_CODE_FOR_MOUSE_SPEED_5            #// v0.3e
holdCmdMorseCode = MORSE_CODE_FOR_HOLD_CMD                        #// v0.3e
releaseCmdMorseCode = MORSE_CODE_FOR_RELEASE_CMD                  #// v0.3e
keycheck = 0
keycodeComboBuff = []     #// v0.3e
lastKeyboardChar = 0      #// v0.3e
lastSentCmdType = 0       #// v0.3e 
flag_hold = 0

morseCodeKeyboard = [
  (".-",    [Keycode.A]), 
  ("-...",  [Keycode.B]),
  ("---.",  [Keycode.C]),
  ("-..",   [Keycode.D]),
  (".",     [Keycode.E]),
  ("..-.",  [Keycode.F]),
  ("--.",   [Keycode.G]),
  ("....",  [Keycode.H]),
  ("..",    [Keycode.I]),
  (".---",  [Keycode.J]),
  ("-.-",   [Keycode.K]),
  (".-..",  [Keycode.L]),
  ("----",  [Keycode.M]),
  ("-.",    [Keycode.N]),
  ("---",   [Keycode.O]),
  (".--.",  [Keycode.P]),
  ("--.-",  [Keycode.Q]),
  (".-.",   [Keycode.R]),
  ("...",   [Keycode.S]),
  ("-",     [Keycode.T]),
  ("..-",   [Keycode.U]),
  ("...-",  [Keycode.V]),
  (".--",   [Keycode.W]),
  ("-..-",  [Keycode.X]),
  ("-.--",  [Keycode.Y]),
  ("--..",  [Keycode.Z]),
  ("-----", [Keycode.ZERO]),
  (".----", [Keycode.ONE]),
  ("..---", [Keycode.TWO]),
  ("...--", [Keycode.THREE]),
  ("....-", [Keycode.FOUR]),
  (".....", [Keycode.FIVE]),
  ("-....", [Keycode.SIX]),
  ("--...", [Keycode.SEVEN]),
  ("---..", [Keycode.EIGHT]),
  ("----.", [Keycode.NINE]),
  ("----..", [Keycode.BACKSLASH]),
  ("....--", [Keycode.FORWARD_SLASH]),
  (".--...", [Keycode.LEFT_BRACKET]),
  ("-..---", [Keycode.RIGHT_BRACKET]),
  ("--..--", [Keycode.SHIFT, Keycode.COMMA]),
  ("..--..", [Keycode.SHIFT, Keycode.PERIOD]),
  ("---...", [Keycode.SHIFT, Keycode.NINE]),
  ("...---", [Keycode.SHIFT, Keycode.ZERO]),
  ("--..-",  [Keycode.SHIFT, Keycode.LEFT_BRACKET]),
  ("--..-",  [Keycode.SHIFT, Keycode.RIGHT_BRACKET]),
  (".-----", [Keycode.PERIOD]),
  ("-.....", [Keycode.COMMA]),
  ("----.-", [Keycode.SHIFT, Keycode.MINUS]),
  ("....-.", [Keycode.SHIFT, Keycode.BACKSLASH]),  
  ("-.----", [Keycode.SHIFT, Keycode.FORWARD_SLASH]),  
  (".-....", [Keycode.SHIFT, Keycode.ONE]),
  ("-....-", [Keycode.SEMICOLON]),
  (".----.", [Keycode.SHIFT, Keycode.SEMICOLON]),
  (".---.",  [Keycode.MINUS]),
  ("..----", [Keycode.SHIFT, Keycode.FOUR]),
  ("...-.-", [Keycode.SHIFT, Keycode.FIVE]),
  ("...--.", [Keycode.SHIFT, Keycode.QUOTE]),
  ("---..-", [Keycode.SHIFT, Keycode.TWO]),
  ("..-...", [Keycode.QUOTE]),  
  ("--.---", [Keycode.GRAVE_ACCENT]),
  ("-...--", [Keycode.SHIFT, Keycode.SIX]),
  ("---.--", [Keycode.SHIFT, Keycode.GRAVE_ACCENT]),
  ("..---.", [Keycode.SHIFT, Keycode.THREE]),
  (".---..", [Keycode.SHIFT, Keycode.SEVEN]),
  ("-...-",  [Keycode.SHIFT,Keycode.EQUALS]),  
  ("---.-",  [Keycode.EQUALS]),  
  ("-..--",  [Keycode.SHIFT, Keycode.EIGHT])
]

morseCodeKeyboard_special = [
  ("..--",    [Keycode.SPACEBAR]),            #// Space
  (".-.-",    [Keycode.ENTER]),           #// Enter           
  (".-.--.",  [Keycode.BACKSPACE]),        #// Backspace         #// v0.3e - changed morse code (older same with mouse down)
  ("--....",  [Keycode.ESCAPE]),           #// ESC  
  ("--...-",  [Keycode.SHIFT]),       #// Shift
  ("-.-.",    [Keycode.LEFT_CONTROL]),     #// Ctrl
  ("--.--",   [Keycode.LEFT_ALT]),         #// Alt
  (".-..-",   [Keycode.UP_ARROW]),         #// Arrow Up
  (".--..",   [Keycode.DOWN_ARROW]),       #// Arrow Down
  (".-.-..",  [Keycode.LEFT_ARROW]),       #// Arrow Left
  (".-.-.",   [Keycode.RIGHT_ARROW]),      #// Arrow Right
  (".....-",  [Keycode.PAGE_UP]),          #// Pg Up 
  ("...-..",  [Keycode.PAGE_DOWN]),        #// Pg Dn
  (".......", [Keycode.HOME]),             #// Home
  ("...-...", [Keycode.END]),              #// End
  ("---...-", [Keycode.KEYPAD_NUMLOCK]),         #// Numlock
  ("--.-..",  [Keycode.SCROLL_LOCK]),      #// ScrollLock
  ("-----.",  [Keycode.CAPS_LOCK]),        #// Capslock
  ("-.-..",   [Keycode.INSERT]),           #// Insert
  ("-.--..",  [Keycode.DELETE]),           #// Delete
  ("--.--.",  [Keycode.PRINT_SCREEN]),     #// PrtScn
  ("---..-.", [Keycode.TAB]),              #// Tab
  ("--.----", [Keycode.F1 ]),               #// F1
  ("--..---", [Keycode.F2 ]),               #// F2
  ("--...--", [Keycode.F3 ]),               #// F3
  ("--....-", [Keycode.F4 ]),               #// F4
  ("--.....", [Keycode.F5 ]),               #// F5
  ("---....", [Keycode.F6 ]),               #// F6
  ("----...", [Keycode.F7 ]),               #// F7
  ("-----..", [Keycode.F8 ]),               #// F8
  ("------.", [Keycode.F9 ]),               #// F9
  ("-------", [Keycode.F10]),              #// F10
  (".------", [Keycode.F11]),              #// F11
  ("..-----", [Keycode.F12]),              #// F12
]

morseCodeMouse = [
    (None,    0),                           #// v0.3e - Just for logic adjustment
    ("...",   MOUSE_MOVE_RIGHT),
    ("..",    MOUSE_MOVE_LEFT),
    ("-",     MOUSE_MOVE_UP),
    ("--",    MOUSE_MOVE_DOWN),
    (".--.",  MOUSE_MOVE_LEFT_UP),          #// v0.3e
    ("...-",  MOUSE_MOVE_RIGHT_UP),         #// v0.3e
    ("...--", MOUSE_MOVE_LEFT_DOWN),        #// v0.3e
    ("...---", MOUSE_MOVE_RIGHT_DOWN),      #// v0.3e
    (".--",   MOUSE_CLICK_RIGHT),
    (".-",    MOUSE_CLICK_LEFT),
    ("..--",  MOUSE_DB_CLICK_RIGHT),
    ("..-",   MOUSE_DB_CLICK_LEFT)
]

morseCodePredefinedStr = [               #// v0.3e
    ("---...-.",      "My name is Morace"),
    ("-..--.",        "No problem"),
    ("-..---.",       "Thank you"),
    ("-.-...--.-..",  "See you later"),
    ("..--..---..",   "How are you?")
]

morseCodeShortcutCmd = [                     #// v0.3e
    ("....----", SHORTCUT_CTRL_C),
    ("...-----", SHORTCUT_CTRL_V),
    ("..--.",    SHORTCUT_WIN_TAB),
    ("..-....",  SHORTCUT_WIN_H)
]

def convertor():
    global keyMouseSwitchMorseCode, swapBleConnectionMorseCode, repeatCmdMorseCode, mouseSpeedIncMorseCode, mouseSpeedDecMorseCode, mouseSpeedSet1MorseCode, mouseSpeedSet5MorseCode, holdCmdMorseCode, releaseCmdMorseCode, lastKeyboardChar, lastSentCmdType, flag_hold
    global morseCodeKeyboard, codeStr, hidMode, flag_repeatCmdEnable
    global k, mouse
    #static uint16_t i;
    i = 0 # local

    if SERIAL_DEBUG_EN:
        print()
        print("Morse Buffer: ", extern.codeStr)        

    if(extern.flag_repeatCmdEnable):           #// v0.3e    
        extern.flag_repeatCmdEnable = 0    
    elif(extern.codeStr == keyMouseSwitchMorseCode):
    
        if(extern.hidMode == KEYBOARD_MODE):        
            extern.hidMode = MOUSE_MODE;      
            if SERIAL_DEBUG_EN:
                print("MOUSE MODE")
        else:
            extern.hidMode = KEYBOARD_MODE;      
            if SERIAL_DEBUG_EN:
                print("KEYBOARD MODE")
        
        #// Write updated data into FS
        extern.writeDataToFS()                               #// v0.3e

        extern.buzzer_set_state(True)#BUZZER_ON;
        time.sleep(0.4)       #// v0.3f
        extern.buzzer_set_state(False)#BUZZER_OFF;
        time.sleep(0.3)
        extern.buzzer_set_state(True)#BUZZER_ON;
        time.sleep(0.4)
        extern.buzzer_set_state(False)#BUZZER_OFF;
        time.sleep(0.3)
        extern.buzzer_set_state(True)#BUZZER_ON;
        time.sleep(0.2)
        extern.buzzer_set_state(False)#BUZZER_OFF;
        time.sleep(0.1)
        extern.buzzer_set_state(True)#BUZZER_ON;
        time.sleep(0.2)
        extern.buzzer_set_state(False)#BUZZER_OFF;
        time.sleep(0.1)    
    elif(extern.codeStr == swapBleConnectionMorseCode):      #// v0.3    
        pass #handleBleConnectionSwap()    
    elif(extern.codeStr == repeatCmdMorseCode):              #// v0.3e    
        extern.flag_repeatCmdEnable = 1
        if SERIAL_DEBUG_EN:
            print("REPEAT CMD")    
    elif(extern.codeStr == mouseSpeedIncMorseCode):          #// v0.3e    
        extern.mouseMoveStep += MOUSE_SPEED_CHANGE_UNIT
        if(extern.mouseMoveStep > MOUSE_SPEED_UPPER_LIMIT):        
            extern.mouseMoveStep = MOUSE_SPEED_UPPER_LIMIT
        
        #// Write updated data into FS
        extern.writeDataToFS()

        if SERIAL_DEBUG_EN:
            print("Mouse Speed Inc, New: ", extern.mouseMoveStep)        
    
    elif extern.codeStr == mouseSpeedDecMorseCode:          #// v0.3e    
        extern.mouseMoveStep -= MOUSE_SPEED_CHANGE_UNIT
        if extern.mouseMoveStep < MOUSE_SPEED_LOWER_LIMIT:        
            extern.mouseMoveStep = MOUSE_SPEED_LOWER_LIMIT
        
        #// Write updated data into FS
        extern.writeDataToFS()
        
        if SERIAL_DEBUG_EN:
            print("Mouse Speed Dec, New: ", extern.mouseMoveStep)    
    elif extern.codeStr == mouseSpeedSet1MorseCode:          #// v0.3e    
        extern.mouseMoveStep = 1

        #// Write updated data into FS
        extern.writeDataToFS()
            
        if SERIAL_DEBUG_EN:
            print("Mouse Speed Set to 1, New: ", extern.mouseMoveStep)    
    elif extern.codeStr == mouseSpeedSet5MorseCode:          #// v0.3e    
        extern.mouseMoveStep = 5

        #// Write updated data into FS
        extern.writeDataToFS()

        if SERIAL_DEBUG_EN:
            print("Mouse Speed Set to 5, New: ", extern.mouseMoveStep)
    elif extern.codeStr == holdCmdMorseCode:                 #// v0.3e    
        flag_hold = 1        
        if SERIAL_DEBUG_EN:
            print("Cmd: Hold")    
    elif extern.codeStr == releaseCmdMorseCode:              #// v0.3e    
        if flag_hold:
            extern.mouse.release_all()        
            #blehid.mouseButtonRelease()
            flag_hold = 0
            if SERIAL_DEBUG_EN:
                print("Cmd: Release")
        else:        
            if SERIAL_DEBUG_EN:
                print("Release Cmd Error")    
    else:    
        if checkPredefinedStrings():             #// v0.3e
            pass
        elif checkShortcutCommands():         #// v0.3e
            pass
        elif checkSpecialKey():               #// v0.3e
            pass
        elif extern.hidMode == KEYBOARD_MODE:        
            for i in range(len(morseCodeKeyboard)):               #// v0.3e            
                if extern.codeStr == morseCodeKeyboard[i][0]:
                    if SERIAL_DEBUG_EN:
                        print("Char: ", morseCodeKeyboard[i][1])                    
                    key_seq_press(extern.k, morseCodeKeyboard[i][1])
                    #blehid.keyPress(morseCodeKeyboard[i][1])
                    time.sleep(0.02)
                    lastSentCmdType = REG_KEYBOARD_CHAR                                #// v0.3e
                    lastKeyboardChar = morseCodeKeyboard[i][1]                   #// v0.3e
                    #blehid.keyRelease()
                    
                    break                            

            if i >= len(morseCodeKeyboard):            
                if SERIAL_DEBUG_EN:
                    print("<Wrong input>")
        else:        
            handleMouseMorseCode()     

    extern.codeStr = ""           #// v0.3e    

def hidSpecialKeyPress(buff):           #// v0.3e
    global keycodeComboBuff
    key_seq_press(extern.k, buff)
    time.sleep(0.02)    

    keycodeComboBuff = []

def handleMouseMorseCode():
    global lastSentCmdType, flag_hold, morseCodeMouse, codeStr, flag_mouseConMovement, mouse
 
    if extern.codeStr == morseCodeMouse[MOUSE_MOVE_RIGHT][0]:    
        lastSentCmdType = MOUSE_CMD              #// v0.3e
        extern.flag_mouseConMovement = MOUSE_MOVE_RIGHT; #// v0.3
        extern.mouse.move(extern.mouseMoveStep, 0)
        #blehid.mouseMove(mouseMoveStep, 0)
        if SERIAL_DEBUG_EN:
            print("Mouse: Right")    
    elif extern.codeStr == morseCodeMouse[MOUSE_MOVE_LEFT][0]:
        lastSentCmdType = MOUSE_CMD              #// v0.3e
        extern.flag_mouseConMovement = MOUSE_MOVE_LEFT  #// v0.3
        extern.mouse.move(-extern.mouseMoveStep, 0)
        #blehid.mouseMove(-mouseMoveStep, 0)        
        if SERIAL_DEBUG_EN:
            print("Mouse: Left")            
    elif extern.codeStr == morseCodeMouse[MOUSE_MOVE_UP][0]:    
        lastSentCmdType = MOUSE_CMD              #// v0.3e
        extern.flag_mouseConMovement = MOUSE_MOVE_UP    #// v0.3
        extern.mouse.move(0, -extern.mouseMoveStep)
        #blehid.mouseMove(0, -mouseMoveStep)
        if SERIAL_DEBUG_EN:
            print("Mouse: Up")            
    elif extern.codeStr == morseCodeMouse[MOUSE_MOVE_DOWN][0]:    
        lastSentCmdType = MOUSE_CMD              #// v0.3e
        extern.flag_mouseConMovement = MOUSE_MOVE_DOWN  #// v0.3      
        extern.mouse.move(0, extern.mouseMoveStep)
        #blehid.mouseMove(0, mouseMoveStep)
        if SERIAL_DEBUG_EN:
            print("Mouse: Down")    
    elif extern.codeStr == morseCodeMouse[MOUSE_MOVE_LEFT_UP][0]:     #// v0.3e    
        lastSentCmdType = MOUSE_CMD
        extern.flag_mouseConMovement = MOUSE_MOVE_LEFT_UP
        extern.mouse.move(-extern.mouseMoveStep, -extern.mouseMoveStep)
        #blehid.mouseMove(-mouseMoveStep, -mouseMoveStep)
        if SERIAL_DEBUG_EN:
            print("Mouse: Left-Up")            
    elif extern.codeStr == morseCodeMouse[MOUSE_MOVE_RIGHT_UP][0]:     #// v0.3e    
        lastSentCmdType = MOUSE_CMD
        extern.flag_mouseConMovement = MOUSE_MOVE_RIGHT_UP
        extern.mouse.move(extern.mouseMoveStep, -extern.mouseMoveStep)
        #blehid.mouseMove(mouseMoveStep, -mouseMoveStep)
        if SERIAL_DEBUG_EN:
            print("Mouse: Right-Up")            
    elif extern.codeStr == morseCodeMouse[MOUSE_MOVE_LEFT_DOWN][0]:     #// v0.3e    
        lastSentCmdType = MOUSE_CMD
        extern.flag_mouseConMovement = MOUSE_MOVE_LEFT_DOWN
        extern.mouse.move(-extern.mouseMoveStep, extern.mouseMoveStep)
        #blehid.mouseMove(-mouseMoveStep, mouseMoveStep)
        if SERIAL_DEBUG_EN:
            print("Mouse: Left-Down")            
    elif extern.codeStr == morseCodeMouse[MOUSE_MOVE_RIGHT_DOWN][0]:     #// v0.3e    
        lastSentCmdType = MOUSE_CMD
        extern.flag_mouseConMovement = MOUSE_MOVE_RIGHT_DOWN
        extern.mouse.move(extern.mouseMoveStep, extern.mouseMoveStep)
        #blehid.mouseMove(mouseMoveStep, mouseMoveStep)
        if SERIAL_DEBUG_EN:
            print("Mouse: Right-Down")    
    elif extern.codeStr == morseCodeMouse[MOUSE_CLICK_RIGHT][0]:
        extern.mouse.press(Mouse.RIGHT_BUTTON)
        #blehid.mouseButtonPress(MOUSE_BUTTON_RIGHT)
        if(not flag_hold):                                    #// v0.3e        
            time.sleep(0.02)
            extern.mouse.release_all()
            #blehid.mouseButtonRelease()        
        if SERIAL_DEBUG_EN:
            print("Mouse: Right Click")    
    elif extern.codeStr == morseCodeMouse[MOUSE_CLICK_LEFT][0]:
        extern.mouse.press(Mouse.LEFT_BUTTON)
        #blehid.mouseButtonPress(MOUSE_BUTTON_LEFT)
        if(not flag_hold):                                    #// v0.3e        
            time.sleep(0.02)
            extern.mouse.release_all()
            #blehid.mouseButtonRelease()        
        if SERIAL_DEBUG_EN:
            print("Mouse: Left Click")            
    elif extern.codeStr == morseCodeMouse[MOUSE_DB_CLICK_RIGHT][0]:
        extern.mouse.press(Mouse.RIGHT_BUTTON)
        #blehid.mouseButtonPress(MOUSE_BUTTON_RIGHT)
        time.sleep(0.05)
        extern.mouse.release_all()
        #blehid.mouseButtonRelease()

        extern.mouse.press(Mouse.RIGHT_BUTTON)
        #blehid.mouseButtonPress(MOUSE_BUTTON_RIGHT)
        time.sleep(0.05)
        extern.mouse.release_all()
        #blehid.mouseButtonRelease()
        print("Mouse: Right Double Click")
        if SERIAL_DEBUG_EN:
            print("Mouse: Right Double Click")
    elif extern.codeStr == morseCodeMouse[MOUSE_DB_CLICK_LEFT][0]:  
        extern.mouse.press(Mouse.RIGHT_BUTTON)  
        #blehid.mouseButtonPress(MOUSE_BUTTON_LEFT)
        time.sleep(0.05)
        extern.mouse.release_all()
        #blehid.mouseButtonRelease()

        extern.mouse.press(Mouse.RIGHT_BUTTON)
        #blehid.mouseButtonPress(MOUSE_BUTTON_LEFT)
        time.sleep(0.05)
        extern.mouse.release_all()
        #blehid.mouseButtonRelease()
        if SERIAL_DEBUG_EN:
            print("Mouse: Left Double Click")    
    else:    
        if SERIAL_DEBUG_EN:
            print("<Wrong Input>")    

def checkPredefinedStrings():                    #// v0.3e
    global morseCodePredefinedStr, codeStr, kl
    j = 0 #local
    for j in range(len(morseCodePredefinedStr)):      
        if extern.codeStr == morseCodePredefinedStr[j][0]:        
            if SERIAL_DEBUG_EN:
                print("Predfined Str: ", morseCodePredefinedStr[j][1])
            extern.kl.write(morseCodePredefinedStr[j][1])
            return 1    
    return 0

def checkShortcutCommands():                       #// v0.3e
    global keycodeComboBuff, morseCodeShortcutCmd, codeStr
    if extern.codeStr == morseCodeShortcutCmd[SHORTCUT_CTRL_C][0]:    
        if SERIAL_DEBUG_EN:
            print("Shortcut Cmd: CTRL+C")

        keycodeComboBuff.append(Keycode.LEFT_CONTROL) #HID_KEY_CONTROL_LEFT
        keycodeComboBuff.append(Keycode.C) #HID_KEY_C
        hidSpecialKeyPress(keycodeComboBuff)    
    elif extern.codeStr == morseCodeShortcutCmd[SHORTCUT_CTRL_V][0]:    
        if SERIAL_DEBUG_EN:
            print("Shortcut Cmd: CTRL+V")        

        keycodeComboBuff.append(Keycode.LEFT_CONTROL) #HID_KEY_CONTROL_LEFT
        keycodeComboBuff.append(Keycode.V) #HID_KEY_V
        hidSpecialKeyPress(keycodeComboBuff)    
    elif extern.codeStr == morseCodeShortcutCmd[SHORTCUT_WIN_TAB][0]:    
        if SERIAL_DEBUG_EN:
            print("Shortcut Cmd: WIN+TAB")        

        keycodeComboBuff.append(Keycode.LEFT_GUI) #HID_KEY_GUI_LEFT
        keycodeComboBuff.append(Keycode.TAB) #HID_KEY_TAB
        hidSpecialKeyPress(keycodeComboBuff)    
    elif extern.codeStr == morseCodeShortcutCmd[SHORTCUT_WIN_H][0]:    
        if SERIAL_DEBUG_EN:      
            print("Shortcut Cmd: WIN+H")

        keycodeComboBuff.append(Keycode.LEFT_GUI) #HID_KEY_GUI_LEFT
        keycodeComboBuff.append(Keycode.H) #HID_KEY_H
        hidSpecialKeyPress(keycodeComboBuff)    
    else:    
        return 0    

    return 1

def checkSpecialKey():                             #// v0.3e
    global keycodeComboBuff, lastSentCmdType, morseCodeKeyboard_special, lastKeyboardChar, codeStr
    i = 0 #local    
    for i in range(len(morseCodeKeyboard_special)):              
        if extern.codeStr == morseCodeKeyboard_special[i][0]:                    
            keycodeComboBuff = morseCodeKeyboard_special[i][1]
            lastSentCmdType = SPL_KEYBOARD_CHAR
            lastKeyboardChar = keycodeComboBuff
            hidSpecialKeyPress(keycodeComboBuff)     
            
            return 1        
    
    return 0


def handleSwitchControlKeypress(void):                          #// v0.3
    return # temp
    global keycheck, ONE_BUTTON_MODE, TWO_BUTTON_MODE, THREE_BUTTON_MODE, button_one_pin, button_two_pin, button_three_pin, k
    if ONE_BUTTON_MODE:
        if extern.button_one_pin.value == False:        
            if keycheck:            
                extern.buzzer_set_state(True) #BUZZER_ON                    #// v0.3f
                keycheck = 0
                extern.k.send(Keycode.SPACE)
                time.sleep(0.05)                
                extern.k.release_all()
                extern.buzzer_set_state(False)#BUZZER_OFF                  #// v0.3f                    
        else:        
            keycheck = 1

    if TWO_BUTTON_MODE:
        if extern.button_one_pin.value == False:
        
            if keycheck:            
                extern.buzzer_set_state(True)#BUZZER_ON                    #// v0.3f
                keycheck = 0
                extern.k.send(Keycode.SPACE)
                time.sleep(0.05)
                extern.k.release_all()
                extern.buzzer_set_state(False)#BUZZER_OFF                   #// v0.3f            
        
        elif extern.button_two_pin.value == False:        
            if keycheck:            
                extern.buzzer_set_state(True)#BUZZER_ON                    #// v0.3f
                keycheck = 0
                extern.k.send(Keycode.ENTER)
                time.sleep(0.05)
                extern.k.release_all()
                extern.buzzer_set_state(False)#BUZZER_OFF                   #// v0.3f                    
        else:         
            keycheck = 1

    if THREE_BUTTON_MODE:
        if extern.button_one_pin.value == False:
            if keycheck:            
                extern.buzzer_set_state(True)#BUZZER_ON                    #// v0.3f
                keycheck = 0
                extern.k.send(Keycode.SPACE)
                time.sleep(0.05)
                extern.k.release_all()
                extern.buzzer_set_state(False)#BUZZER_OFF                   #// v0.3f                    
        elif extern.button_two_pin.value == False:        
            if keycheck:
                extern.buzzer_set_state(True)#BUZZER_ON                    #// v0.3f
                keycheck = 0
                extern.k.send(Keycode.ENTER)
                time.sleep(0.05)
                extern.k.release_all()
                extern.buzzer_set_state(False)#BUZZER_OFF                   #// v0.3f
        elif extern.button_three_pin.value == False:
            if keycheck:
                extern.buzzer_set_state(True)#BUZZER_ON                    #// v0.3f
                keycheck = 0
                extern.k.send(Keycode.BACKSPACE)                       
                time.sleep(0.05)
                extern.k.release_all()
                extern.buzzer_set_state(False)#BUZZER_OFF                   #// v0.3f
        else:
            keycheck = 1

def findDotOrDash():
    global dotLength, DOT, DASH, signal_len
    if extern.signal_len <= dotLength:
        return DOT
    else:
        return DASH

def findDot():
    global dotLength, DOT, signal_len
    if extern.signal_len <= dotLength:
        return DOT    
    else:    
        return None

def findDash():
    global dotLength, DASH, signal_len
    if extern.signal_len <= dotLength:
        return None
    else:
        return DASH

def handleConMouseMovement():    #// v0.3
    global flag_mouseConMovement, mouse
    if extern.flag_mouseConMovement == MOUSE_MOVE_RIGHT:
        extern.mouse.move(extern.mouseMoveStep, 0)
        
    elif extern.flag_mouseConMovement == MOUSE_MOVE_LEFT:
        extern.mouse.move(-extern.mouseMoveStep, 0)
        
    elif extern.flag_mouseConMovement == MOUSE_MOVE_UP:
        extern.mouse.move(0, -extern.mouseMoveStep)
        
    elif extern.flag_mouseConMovement == MOUSE_MOVE_DOWN:
        extern.mouse.move(0, extern.mouseMoveStep)
        
    elif extern.flag_mouseConMovement == MOUSE_MOVE_LEFT_UP:        #// v0.3e
        extern.mouse.move(-extern.mouseMoveStep, -extern.mouseMoveStep)
        
    elif extern.flag_mouseConMovement == MOUSE_MOVE_RIGHT_UP:       #// v0.3e
        extern.mouse.move(extern.mouseMoveStep, -extern.mouseMoveStep)
        
    elif extern.flag_mouseConMovement == MOUSE_MOVE_LEFT_DOWN:      #// v0.3e
        extern.mouse.move(-extern.mouseMoveStep, extern.mouseMoveStep)
        
    elif extern.flag_mouseConMovement == MOUSE_MOVE_RIGHT_DOWN:     #// v0.3e
        extern.mouse.move(extern.mouseMoveStep, extern.mouseMoveStep)
        
def handleRepeatCmdAction():     #// v0.3e
    global keycodeComboBuff, lastSentCmdType, lastKeyboardChar
    if lastSentCmdType == REG_KEYBOARD_CHAR:
        key_seq_press(extern.k, lastKeyboardChar)
        time.sleep(0.02)
        extern.k.release_all()
    elif lastSentCmdType == SPL_KEYBOARD_CHAR:
        keycodeComboBuff[0] = lastKeyboardChar        
        hidSpecialKeyPress(keycodeComboBuff)
    elif lastSentCmdType == MOUSE_CMD:
        handleConMouseMovement()
