import time

from userConfig import *
import extern

if x80_pinout:
    from x80PinMap import *
else:
    from userPinMap import *

from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

def key_seq_press(kb_obj, key_seq):
    for keycode in key_seq:
        kb_obj._add_keycode_to_report(keycode)
        kb_obj._keyboard_device.send_report(kb_obj.report)
    kb_obj.release_all()

keycheck = 0
keycodeComboBuff = []     #// v0.3e
lastKeyboardChar = 0      #// v0.3e
lastSentCmdType = 0       #// v0.3e
flag_hold = 0
mouse_buttons_state = 0

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
  ("--",  [Keycode.M]),
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
  ("..--",    [Keycode.SPACEBAR]),         #// Space
  (".-.-",    [Keycode.ENTER]),            #// Enter
  (".-.--.",  [Keycode.BACKSPACE]),        #// Backspace
  ("--....",  [Keycode.ESCAPE]),           #// ESC
  ("--...-",  [Keycode.SHIFT]),            #// Shift
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
  ("---...-", [Keycode.KEYPAD_NUMLOCK]),   #// Numlock
  ("--.-..",  [Keycode.SCROLL_LOCK]),      #// ScrollLock
  ("-----.",  [Keycode.CAPS_LOCK]),        #// Capslock
  ("-.-..",   [Keycode.INSERT]),           #// Insert
  ("-.--..",  [Keycode.DELETE]),           #// Delete
  ("--.--.",  [Keycode.PRINT_SCREEN]),     #// PrtScn
  ("---..-.", [Keycode.TAB]),              #// Tab
  (".--.--",  [Keycode.LEFT_GUI]),         #// LGUI/Windows/Mac
  ("--.----", [Keycode.F1 ]),              #// F1
  ("--..---", [Keycode.F2 ]),              #// F2
  ("--...--", [Keycode.F3 ]),              #// F3
  ("--....-", [Keycode.F4 ]),              #// F4
  ("--.....", [Keycode.F5 ]),              #// F5
  ("---....", [Keycode.F6 ]),              #// F6
  ("----...", [Keycode.F7 ]),              #// F7
  ("-----..", [Keycode.F8 ]),              #// F8
  ("------.", [Keycode.F9 ]),              #// F9
  ("-------", [Keycode.F10]),              #// F10
  (".------", [Keycode.F11]),              #// F11
  ("..-----", [Keycode.F12]),              #// F12
]

mouse_move_right       = 1
mouse_move_left        = 2
mouse_move_up          = 3
mouse_move_down        = 4
mouse_move_left_up     = 5
mouse_move_right_up    = 6
mouse_move_left_down   = 7
mouse_move_right_down  = 8
mouse_click_right      = 9
mouse_click_left       = 10
mouse_db_click_right   = 11
mouse_db_click_left    = 12
mouse_press_hold_right = 13
mouse_press_hold_left  = 14

morseCodeMouse = [
    (None,    0),                           #// v0.3e - Just for logic adjustment
    ("...",    mouse_move_right),
    ("..",     mouse_move_left),
    ("-",      mouse_move_up),
    ("--",     mouse_move_down),
    (".--.",   mouse_move_left_up),          #// v0.3e
    ("...-",   mouse_move_right_up),         #// v0.3e
    ("...--",  mouse_move_left_down),        #// v0.3e
    ("...---", mouse_move_right_down),      #// v0.3e
    (".--",    mouse_click_right),
    (".-",     mouse_click_left),
    ("..--",   mouse_db_click_right),
    ("..-",    mouse_db_click_left),
    ("..--.",  mouse_press_hold_right),
    ("..-.",   mouse_press_hold_left)
]

morseCodePredefinedStr = [                  #// v0.3e
    ("---...-.",      "My name is Morace"),
    ("-..--.",        "No problem"),
    ("-..---.",       "Thank you"),
    ("-.-...--.-..",  "See you later"),
    ("..--..---..",   "How are you?")
]

shortcut_ctrl_c  = 0
shortcut_ctrl_v  = 1
shortcut_win_tab = 2
shortcut_win_h   = 3

morseCodeShortcutCmd = [                    #// v0.3e
    ("....----", shortcut_ctrl_c),
    ("...-----", shortcut_ctrl_v),
    ("..--.",    shortcut_win_tab),
    ("..-....",  shortcut_win_h)
]

reg_keyboard_char = 0
spl_keyboard_char = 1
mouse_cmd         = 2

def convertor():
    global keyMouseSwitchMorseCode, swapBleConnectionMorseCode, repeatCmdMorseCode, mouseSpeedIncMorseCode, mouseSpeedDecMorseCode, mouseSpeedSet1MorseCode, mouseSpeedSet5MorseCode, holdCmdMorseCode, releaseCmdMorseCode, lastKeyboardChar, lastSentCmdType, flag_hold
    global morseCodeKeyboard, mouse_buttons_state

    i = 0 # local

    if serial_debug_en:
        print()
        print("Morse Buffer: ", extern.codeStr)

    if(extern.flag_repeatCmdEnable):           #// v0.3e
        extern.flag_repeatCmdEnable = 0
    elif(extern.codeStr == keyMouseSwitchMorseCode):

        if(extern.hidMode == keyboard_mode):
            extern.hidMode = mouse_mode
            if serial_debug_en:
                print("MOUSE MODE")
        else:
            extern.hidMode = keyboard_mode
            if serial_debug_en:
                print("KEYBOARD MODE")

        #// Write updated data into FS
        extern.writeDataToFS()                               #// v0.3e

        extern.buzzer_activate(buzzer_freq)
        time.sleep(0.4)       #// v0.3f
        extern.buzzer_deactivate()
        time.sleep(0.3)
        extern.buzzer_activate(buzzer_freq)
        time.sleep(0.4)
        extern.buzzer_deactivate()
        time.sleep(0.3)
        extern.buzzer_activate(buzzer_freq)
        time.sleep(0.2)
        extern.buzzer_deactivate()
        time.sleep(0.1)
        extern.buzzer_activate(buzzer_freq)
        time.sleep(0.2)
        extern.buzzer_deactivate()
        time.sleep(0.1)
    elif(extern.codeStr == swapBleConnectionMorseCode):      #// v0.3
        extern.handleBleConnectionSwap()
    elif(extern.codeStr == mouseSpeedIncMorseCode):          #// v0.3e
        extern.mouseMoveStep += mouse_speed_change_unit
        if(extern.mouseMoveStep > mouse_speed_upper_limit):
            extern.mouseMoveStep = mouse_speed_upper_limit

        #// Write updated data into FS
        extern.writeDataToFS()

        if serial_debug_en:
            print("Mouse Speed Inc, New: ", extern.mouseMoveStep)

    elif extern.codeStr == mouseSpeedDecMorseCode:          #// v0.3e
        extern.mouseMoveStep -= mouse_speed_change_unit
        if extern.mouseMoveStep < mouse_speed_lower_limit:
            extern.mouseMoveStep = mouse_speed_lower_limit

        #// Write updated data into FS
        extern.writeDataToFS()

        if serial_debug_en:
            print("Mouse Speed Dec, New: ", extern.mouseMoveStep)
    elif extern.codeStr == mouseSpeedSet1MorseCode:          #// v0.3e
        extern.mouseMoveStep = 1

        #// Write updated data into FS
        extern.writeDataToFS()

        if serial_debug_en:
            print("Mouse Speed Set to 1, New: ", extern.mouseMoveStep)
    elif extern.codeStr == mouseSpeedSet5MorseCode:          #// v0.3e
        extern.mouseMoveStep = 5

        #// Write updated data into FS
        extern.writeDataToFS()

        if serial_debug_en:
            print("Mouse Speed Set to 5, New: ", extern.mouseMoveStep)
    elif extern.codeStr == holdCmdMorseCode:                 #// v0.3e
        flag_hold = 1
        if serial_debug_en:
            print("Cmd: Hold")
    elif extern.codeStr == releaseCmdMorseCode:              #// v0.3e
        extern.mouse.release_all()
        mouse_buttons_state = 0
        flag_hold = 0
        if serial_debug_en:
            print("Cmd: Release")

    else:
        if extern.hidMode == keyboard_mode:
            if extern.codeStr == repeatKeybCmdMorseCode and lastSentCmdType != mouse_cmd:
                extern.flag_repeatCmdEnable = 1
                if serial_debug_en:
                    print("REPEAT KEYBOARD CMD")
            if checkPredefinedStrings():             #// v0.3e
                pass
            elif checkShortcutCommands():         #// v0.3e
                pass
            elif checkSpecialKey():               #// v0.3e
                pass
            else:
                for i in range(len(morseCodeKeyboard)):               #// v0.3e
                    if extern.codeStr == morseCodeKeyboard[i][0]:
                        if serial_debug_en:
                            print("Char: ", morseCodeKeyboard[i][1])
                        key_seq_press(extern.k, morseCodeKeyboard[i][1])
                        time.sleep(0.02)
                        lastSentCmdType = reg_keyboard_char                                #// v0.3e
                        lastKeyboardChar = morseCodeKeyboard[i][1]                   #// v0.3e

                        break

                if i >= len(morseCodeKeyboard):
                    if serial_debug_en:
                        print("<Wrong input>")
        else:
            if extern.codeStr == repeatMouseCmdMorseCode and lastSentCmdType == mouse_cmd:
                extern.flag_repeatCmdEnable = 1
                if serial_debug_en:
                    print("REPEAT MOUSE CMD")
            else:
                handleMouseMorseCode()

    extern.codeStr = ""           #// v0.3e

def hidSpecialKeyPress(buff):           #// v0.3e
    global keycodeComboBuff
    key_seq_press(extern.k, buff)
    time.sleep(0.02)

    keycodeComboBuff = []

def handleMouseMorseCode():
    global lastSentCmdType, flag_hold, morseCodeMouse, mouse_buttons_state

    if extern.codeStr == morseCodeMouse[mouse_move_right][0]:
        lastSentCmdType = mouse_cmd                      #// v0.3e
        extern.flag_mouseConMovement = mouse_move_right; #// v0.3
        extern.mouse.move(extern.mouseMoveStep, 0)
        if serial_debug_en:
            print("Mouse: Right")
    elif extern.codeStr == morseCodeMouse[mouse_move_left][0]:
        lastSentCmdType = mouse_cmd                     #// v0.3e
        extern.flag_mouseConMovement = mouse_move_left  #// v0.3
        extern.mouse.move(-extern.mouseMoveStep, 0)
        if serial_debug_en:
            print("Mouse: Left")
    elif extern.codeStr == morseCodeMouse[mouse_move_up][0]:
        lastSentCmdType = mouse_cmd                     #// v0.3e
        extern.flag_mouseConMovement = mouse_move_up    #// v0.3
        extern.mouse.move(0, -extern.mouseMoveStep)
        if serial_debug_en:
            print("Mouse: Up")
    elif extern.codeStr == morseCodeMouse[mouse_move_down][0]:
        lastSentCmdType = mouse_cmd                     #// v0.3e
        extern.flag_mouseConMovement = mouse_move_down  #// v0.3
        extern.mouse.move(0, extern.mouseMoveStep)
        if serial_debug_en:
            print("Mouse: Down")
    elif extern.codeStr == morseCodeMouse[mouse_move_left_up][0]:       #// v0.3e
        lastSentCmdType = mouse_cmd
        extern.flag_mouseConMovement = mouse_move_left_up
        extern.mouse.move(-extern.mouseMoveStep, -extern.mouseMoveStep)
        if serial_debug_en:
            print("Mouse: Left-Up")
    elif extern.codeStr == morseCodeMouse[mouse_move_right_up][0]:      #// v0.3e
        lastSentCmdType = mouse_cmd
        extern.flag_mouseConMovement = mouse_move_right_up
        extern.mouse.move(extern.mouseMoveStep, -extern.mouseMoveStep)
        if serial_debug_en:
            print("Mouse: Right-Up")
    elif extern.codeStr == morseCodeMouse[mouse_move_left_down][0]:     #// v0.3e
        lastSentCmdType = mouse_cmd
        extern.flag_mouseConMovement = mouse_move_left_down
        extern.mouse.move(-extern.mouseMoveStep, extern.mouseMoveStep)
        if serial_debug_en:
            print("Mouse: Left-Down")
    elif extern.codeStr == morseCodeMouse[mouse_move_right_down][0]:    #// v0.3e
        lastSentCmdType = mouse_cmd
        extern.flag_mouseConMovement = mouse_move_right_down
        extern.mouse.move(extern.mouseMoveStep, extern.mouseMoveStep)
        if serial_debug_en:
            print("Mouse: Right-Down")
    elif extern.codeStr == morseCodeMouse[mouse_click_right][0]:
        lastSentCmdType = mouse_cmd
        extern.mouse.press(Mouse.RIGHT_BUTTON)
        time.sleep(0.02)
        extern.mouse.release_all()

        mouse_buttons_state = 0

        if serial_debug_en:
            print("Mouse: Right Click")
    elif extern.codeStr == morseCodeMouse[mouse_click_left][0]:
        lastSentCmdType = mouse_cmd
        extern.mouse.press(Mouse.LEFT_BUTTON)
        time.sleep(0.02)
        extern.mouse.release_all()

        mouse_buttons_state = 0

        if serial_debug_en:
            print("Mouse: Left Click")
    elif extern.codeStr == morseCodeMouse[mouse_db_click_right][0]:
        lastSentCmdType = mouse_cmd
        extern.mouse.press(Mouse.RIGHT_BUTTON)
        time.sleep(0.05)
        extern.mouse.release_all()

        extern.mouse.press(Mouse.RIGHT_BUTTON)
        time.sleep(0.05)
        extern.mouse.release_all()

        mouse_buttons_state = 0

        if serial_debug_en:
            print("Mouse: Right Double Click")
    elif extern.codeStr == morseCodeMouse[mouse_db_click_left][0]:
        lastSentCmdType = mouse_cmd
        extern.mouse.press(Mouse.LEFT_BUTTON)
        time.sleep(0.05)
        extern.mouse.release_all()

        extern.mouse.press(Mouse.LEFT_BUTTON)
        time.sleep(0.05)
        extern.mouse.release_all()

        mouse_buttons_state = 0

        if serial_debug_en:
            print("Mouse: Left Double Click")
    elif extern.codeStr == morseCodeMouse[mouse_press_hold_right][0]:
        lastSentCmdType = mouse_cmd
        if mouse_buttons_state != Mouse.RIGHT_BUTTON:
            extern.mouse.press(Mouse.RIGHT_BUTTON)
            mouse_buttons_state = Mouse.RIGHT_BUTTON
        else:
            extern.mouse.release_all()
            mouse_buttons_state = 0

        if serial_debug_en:
            print("Mouse: Right press & hold")
    elif extern.codeStr == morseCodeMouse[mouse_press_hold_left][0]:
        lastSentCmdType = mouse_cmd
        if mouse_buttons_state != Mouse.LEFT_BUTTON:
            extern.mouse.press(Mouse.LEFT_BUTTON)
            mouse_buttons_state = Mouse.LEFT_BUTTON
        else:
            extern.mouse.release_all()
            mouse_buttons_state = 0

        if serial_debug_en:
            print("Mouse: Left press & hold")
    else:
        if serial_debug_en:
            print("<Wrong Input>")

def checkPredefinedStrings():                    #// v0.3e
    global morseCodePredefinedStr
    j = 0 #local
    for j in range(len(morseCodePredefinedStr)):
        if extern.codeStr == morseCodePredefinedStr[j][0]:
            if serial_debug_en:
                print("Predfined Str: ", morseCodePredefinedStr[j][1])
            extern.kl.write(morseCodePredefinedStr[j][1])
            return 1
    return 0

def checkShortcutCommands():                       #// v0.3e
    global keycodeComboBuff, morseCodeShortcutCmd
    if extern.codeStr == morseCodeShortcutCmd[shortcut_ctrl_c][0]:
        if serial_debug_en:
            print("Shortcut Cmd: CTRL+C")

        keycodeComboBuff.append(Keycode.LEFT_CONTROL)
        keycodeComboBuff.append(Keycode.C)
        hidSpecialKeyPress(keycodeComboBuff)
    elif extern.codeStr == morseCodeShortcutCmd[shortcut_ctrl_v][0]:
        if serial_debug_en:
            print("Shortcut Cmd: CTRL+V")

        keycodeComboBuff.append(Keycode.LEFT_CONTROL)
        keycodeComboBuff.append(Keycode.V)
        hidSpecialKeyPress(keycodeComboBuff)
    elif extern.codeStr == morseCodeShortcutCmd[shortcut_win_tab][0]:
        if serial_debug_en:
            print("Shortcut Cmd: WIN+TAB")

        keycodeComboBuff.append(Keycode.LEFT_GUI)
        keycodeComboBuff.append(Keycode.TAB)
        hidSpecialKeyPress(keycodeComboBuff)
    elif extern.codeStr == morseCodeShortcutCmd[shortcut_win_h][0]:
        if serial_debug_en:
            print("Shortcut Cmd: WIN+H")

        keycodeComboBuff.append(Keycode.LEFT_GUI)
        keycodeComboBuff.append(Keycode.H)
        hidSpecialKeyPress(keycodeComboBuff)
    else:
        return 0

    return 1

def checkSpecialKey():                             #// v0.3e
    global keycodeComboBuff, lastSentCmdType, morseCodeKeyboard_special, lastKeyboardChar
    i = 0 #local
    for i in range(len(morseCodeKeyboard_special)):
        if extern.codeStr == morseCodeKeyboard_special[i][0]:
            keycodeComboBuff = morseCodeKeyboard_special[i][1]
            lastSentCmdType = spl_keyboard_char
            lastKeyboardChar = keycodeComboBuff
            hidSpecialKeyPress(keycodeComboBuff)

            return 1

    return 0


def handleSwitchControlKeypress():                          #// v0.3
    global keycheck, one_button_mode, two_button_mode, three_button_mode
    if one_button_mode:
        if extern.button_one.value == False:
            if keycheck:
                extern.buzzer_activate(buzzer_freq)                    #// v0.3f
                keycheck = 0
                extern.k.send(Keycode.SPACE)
                time.sleep(0.05)
                extern.k.release_all()
                extern.buzzer_deactivate()                  #// v0.3f
        else:
            keycheck = 1

    if two_button_mode:
        if extern.button_one.value == False:

            if keycheck:
                extern.buzzer_activate(buzzer_freq)                    #// v0.3f
                keycheck = 0
                extern.k.send(Keycode.SPACE)
                time.sleep(0.05)
                extern.k.release_all()
                extern.buzzer_deactivate()                   #// v0.3f

        elif extern.button_two.value == False:
            if keycheck:
                extern.buzzer_activate(buzzer_freq)                    #// v0.3f
                keycheck = 0
                extern.k.send(Keycode.ENTER)
                time.sleep(0.05)
                extern.k.release_all()
                extern.buzzer_deactivate()                   #// v0.3f
        else:
            keycheck = 1

    if three_button_mode:
        if extern.button_one.value == False:
            if keycheck:
                extern.buzzer_activate(buzzer_freq)                    #// v0.3f
                keycheck = 0
                extern.k.send(Keycode.SPACE)
                time.sleep(0.05)
                extern.k.release_all()
                extern.buzzer_deactivate()                   #// v0.3f
        elif extern.button_two.value == False:
            if keycheck:
                extern.buzzer_activate(buzzer_freq)                    #// v0.3f
                keycheck = 0
                extern.k.send(Keycode.ENTER)
                time.sleep(0.05)
                extern.k.release_all()
                extern.buzzer_deactivate()                   #// v0.3f
        elif extern.button_three.value == False:
            if keycheck:
                extern.buzzer_activate(buzzer_freq)                    #// v0.3f
                keycheck = 0
                extern.k.send(Keycode.BACKSPACE)
                time.sleep(0.05)
                extern.k.release_all()
                extern.buzzer_deactivate()                   #// v0.3f
        else:
            keycheck = 1

def findDotOrDash():
    global dot_length, dot, dash
    if extern.signal_len <= dot_length:
        return dot
    else:
        return dash

def findDot():
    global dot_length, dot
    if extern.signal_len <= dot_length:
        return dot
    else:
        return None

def findDash():
    global dot_length, dash
    if extern.signal_len <= dot_length:
        return None
    else:
        return dash

def handleConMouseMovement():    #// v0.3
    if extern.flag_mouseConMovement == mouse_move_right:
        extern.mouse.move(extern.mouseMoveStep, 0)

    elif extern.flag_mouseConMovement == mouse_move_left:
        extern.mouse.move(-extern.mouseMoveStep, 0)

    elif extern.flag_mouseConMovement == mouse_move_up:
        extern.mouse.move(0, -extern.mouseMoveStep)

    elif extern.flag_mouseConMovement == mouse_move_down:
        extern.mouse.move(0, extern.mouseMoveStep)

    elif extern.flag_mouseConMovement == mouse_move_left_up:        #// v0.3e
        extern.mouse.move(-extern.mouseMoveStep, -extern.mouseMoveStep)

    elif extern.flag_mouseConMovement == mouse_move_right_up:       #// v0.3e
        extern.mouse.move(extern.mouseMoveStep, -extern.mouseMoveStep)

    elif extern.flag_mouseConMovement == mouse_move_left_down:      #// v0.3e
        extern.mouse.move(-extern.mouseMoveStep, extern.mouseMoveStep)

    elif extern.flag_mouseConMovement == mouse_move_right_down:     #// v0.3e
        extern.mouse.move(extern.mouseMoveStep, extern.mouseMoveStep)

def handleRepeatCmdAction():     #// v0.3e
    global keycodeComboBuff, lastSentCmdType, lastKeyboardChar
    if lastSentCmdType == reg_keyboard_char:
        key_seq_press(extern.k, lastKeyboardChar)
        time.sleep(0.02)
        extern.k.release_all()
    elif lastSentCmdType == spl_keyboard_char:
        keycodeComboBuff = lastKeyboardChar
        hidSpecialKeyPress(keycodeComboBuff)
    elif lastSentCmdType == mouse_cmd:
        handleConMouseMovement()
