import time

from user.config import *
import extern

if x80_pinout:
    from x80PinMap import *
else:
    from userPinMap import *

from user.morse_code import *
from user.morse_code_shortcuts import *

import microcontroller
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

keycheck = 0
keycodeComboBuff = []     #// v0.3e
lastKeyboardChar = 0      #// v0.3e
lastSentCmdType = 0       #// v0.3e
flag_hold = 0
mouse_buttons_state = 0

prev_mode = extern.hidMode

reg_keyboard_char = 0
spl_keyboard_char = 1
mouse_cmd         = 2

def key_seq_press(buff):
    for keycode in buff:
        extern.k._add_keycode_to_report(keycode)
        extern.k._keyboard_device.send_report(extern.k.report)

    extern.k.release_all()
    time.sleep(0.02)

def convertor():
    global keyMouseSwitchMorseCode, swapBleConnectionMorseCode, repeatCmdMorseCode, mouseSpeedIncMorseCode, mouseSpeedDecMorseCode, mouseSpeedSet1MorseCode, mouseSpeedSet5MorseCode, holdCmdMorseCode, releaseCmdMorseCode, lastKeyboardChar, lastSentCmdType, flag_hold
    global morseCodeKeyboard, mouse_buttons_state, prev_mode

    i = 0 # local

    if serial_debug_en:
        print()
        print("Morse Buffer: ", extern.codeStr)

    if extern.flag_repeatCmdEnable:           #// v0.3e
        extern.flag_repeatCmdEnable = 0
    elif extern.codeStr == resetMcuMorseCode:
        microcontroller.reset()
    elif extern.codeStr == keyMouseSwitchMorseCode:

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
    elif extern.codeStr == macro_mode_morse_code:
        prev_mode = extern.hidMode
        extern.hidMode = macro_mode
        if serial_debug_en:
            print("MACRO MODE")
    elif extern.codeStr == swapBleConnectionMorseCode:      #// v0.3
        extern.handleBleConnectionSwap()
    elif extern.codeStr == mouseSpeedIncMorseCode:          #// v0.3e
        extern.mouseMoveStep += mouse_speed_change_unit
        if extern.mouseMoveStep > mouse_speed_upper_limit:
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
            elif checkSpecialKey():               #// v0.3e
                pass
            else:
                for i in range(len(morseCodeKeyboard)):               #// v0.3e
                    if extern.codeStr == morseCodeKeyboard[i][0]:
                        if serial_debug_en:
                            print("Char: ", morseCodeKeyboard[i][1])
                        key_seq_press(morseCodeKeyboard[i][1])
                        time.sleep(0.02)
                        lastSentCmdType = reg_keyboard_char                                #// v0.3e
                        lastKeyboardChar = morseCodeKeyboard[i][1]                   #// v0.3e

                        break

                if i >= len(morseCodeKeyboard):
                    if serial_debug_en:
                        print("<Wrong input>")
        elif extern.hidMode == mouse_mode:
            if extern.codeStr == repeatMouseCmdMorseCode and lastSentCmdType == mouse_cmd:
                extern.flag_repeatCmdEnable = 1
                if serial_debug_en:
                    print("REPEAT MOUSE CMD")
            else:
                handleMouseMorseCode()
        else:
            checkMacroCmds()

            extern.hidMode = prev_mode

    extern.codeStr = ""           #// v0.3e

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

def checkMacroCmds():
    global morseCodeShortcutCmd

    for i in range(len(morseCodeShortcutCmd)):
        if extern.codeStr == morseCodeShortcutCmd[i][0]:
            if serial_debug_en:
                print("Macro: ", morseCodeShortcutCmd[i][1])

            if isinstance(morseCodeShortcutCmd[i][1], list):
                key_seq_press(morseCodeShortcutCmd[i][1])
            elif isinstance(morseCodeShortcutCmd[i][1], str):
                for char in morseCodeShortcutCmd[i][1]:
                    key_seq = keyboard_keymap.get(char)
                    if key_seq != None:
                        key_seq_press(key_seq)

            return 1
    return 0

def checkSpecialKey():                             #// v0.3e
    global keycodeComboBuff, lastSentCmdType, morseCodeKeyboard_special, lastKeyboardChar
    i = 0 #local
    for i in range(len(morseCodeKeyboard_special)):
        if extern.codeStr == morseCodeKeyboard_special[i][0]:
            keycodeComboBuff = morseCodeKeyboard_special[i][1]
            lastSentCmdType = spl_keyboard_char
            lastKeyboardChar = keycodeComboBuff
            key_seq_press(keycodeComboBuff)

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
        key_seq_press(lastKeyboardChar)
        time.sleep(0.02)
        extern.k.release_all()
    elif lastSentCmdType == spl_keyboard_char:
        keycodeComboBuff = lastKeyboardChar
        key_seq_press(keycodeComboBuff)
    elif lastSentCmdType == mouse_cmd:
        handleConMouseMovement()
