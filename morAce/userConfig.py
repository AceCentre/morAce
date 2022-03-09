
from morseCode_h import *

"""
/*  Device Specific Settings
 *  DEVICE_BLE_NAME     : Device will advertise by this name in Morse Mode
 *  DEVICE_BLE_NAME2    : Device will advertise by this name in Switch Control Mode
 *  DEVICE_MANUFACTURER : Manufacturere name in BLE device properties
 *  DEVICE_MODEL_NAME   : Modem name in BLE device properties
 *  
 *  note - Write string between double quotes
 */
"""
DEVICE_BLE_NAME = "MORSE_HID"
DEVICE_BLE_NAME2 = "SW_HID"                #// v0.3c
DEVICE_MANUFACTURER = "ABC"
DEVICE_MODEL_NAME = "BLE-HID-v1"

"""
/*  Device Mode Setting
 *  ONE_BUTTON_MODE   : Only 1st button will be used. Button 2 and button 3 are unused
 *                      1st button itself accept both dots and dashes. 
 *                      And if there is specific amount of time gap between button press then is should be automatically considered as end of character.
 *  TWO_BUTTON_MODE   : 1st and 2nd buttons will be used. Button 3 is unused
 *                      1st button will only accept dots, 2nd button will only accept dashes.
 *                      And if there is specific amount of time gap between button press then is should be automatically considered as end of character.
 *  THREE_BUTTON_MODE : All 3 buttons will be used
 *                      1st button will only accept dots, 2nd button will only accept dashes and 3rd button will be used as end of character.
 *                      So here character ending is manual.
 *                  
 *  note : Any one of three must be present below (ONE_BUTTON_MODE / TWO_BUTTON_MODE / THREE_BUTTON_MODE)
 */
"""
ONE_BUTTON_MODE = 0
TWO_BUTTON_MODE = 1
THREE_BUTTON_MODE = 1


MORSE_MODE = 0
SW_CTRL_MODE = 1
"""
/*  Fast Typing Mode Enable/Disable 
 *  Effective only in Two & Three Button Modes
 *  When Enable, by pressing down a button, device will accept multiple Dots/Dashes depending on press time
 *  
 *  1 - Enable / 0 - Disable
 */
"""
FAST_TYPING_MODE = 0

"""
/*  MORSE Code Settings 
 *  DOT_LENGTH : Unit length of a dot in tearms of milliseconds
 */
"""
DOT_LENGTH = 200

"""
/*  MORSE Code for switching between Keyboard mode and Mouse mode
 *  
 *  note : Write morse code between double quotes
 */
"""
MORSE_CODE_FOR_KEYB_MOUSE_SWITCH = ".-.--"

"""
/*  Default mode for the device : Keyboard Mode / Mouse Mode
 *  
 *  For Keyboard Mode : KEYBOARD_MODE
 *  For Mouse Mode    : MOUSE_MODE
 */
"""
DEFAULT_MODE_OF_DEVICE = MOUSE_MODE

"""
/*  MORSE Code for Swap Connection
 *  
 *  note : Write morse code between double quotes
 */
"""
MORSE_CODE_FOR_BLE_SWAP_CONNECTION  = "-.-.--"

"""
/*  Define timeout for BLE connection swapping
 *  By pressing a switch to swap BLE connection, if device is not connected to another PC till this timeout,
 *  then device will reconnect with older PC.
 *  
 *  note : Define timeout in milliseconds
 */
"""
LAST_CONNECTION_CHECK_TIMEOUT = 10000

"""
/*  Mouse HID - Default Step size for Mouse movement
 *  Mouse cursor will be moved by this step size (If not set by user)
 *  
 *  note : Step must be integer
 */
"""
DEFAULT_MOUSE_MOVE_STEP = 5

"""
/*  Time interval to send mouse movement command in milliseconds
 *  Mouse move command to right/left/up/down will be sent at this interval
 *  
 *  note : Define timeout in milliseconds
 */
"""
INTERVAL_SEND_MOUSE_MOVE_CMD = 100

"""
/*  Maximum allowable BLE connections swaps
 *  
 *  note : Must be <= 5
 */ 
"""

MAXIMUM_SWAP_CONNECTIONS = 4

"""
/*  MORSE Code for REPEAT Command
 *  Previous Morse command (Keyboard Character/Mouse Commands) 
 *  will be repeated after sending this REPEAT command morse code
 *  note : Write morse code between double quotes
 */
"""
MORSE_CODE_FOR_REPEAT_CMD = ".---.-"

"""
/*  MORSE Code for HOLD Command
 *  Send this command first to hold down any key/mouse click
 *  and then after send command for key/mouse clik you want to hold
 *  note : Write morse code between double quotes
 */
"""
MORSE_CODE_FOR_HOLD_CMD = ".---.-."

"""
/*  MORSE Code for RELEASE Command
 *  Send this command to release prevoiusly holded key/mouse click
 *  note : Write morse code between double quotes
 */
"""
MORSE_CODE_FOR_RELEASE_CMD = ".---.--"

"""
/*  Time interval to send REPEAT command in milliseconds
 *  Previous Morse command (Keyboard Character/Mouse Commands)
 *  will be sent at this interval
 *  note : Define timeout in milliseconds
 */
"""
INTERVAL_SEND_REPEAT_CMD = 100

"""
/*  MORSE Code for Mouse Speed Increase
 *  
 *  note : Write morse code between double quotes
 */
"""

MORSE_CODE_FOR_MOUSE_SPEED_INC = ".-..--"

"""
/*  MORSE Code for Mouse Speed Decrease
 *  
 *  note : Write morse code between double quotes
 */
"""

MORSE_CODE_FOR_MOUSE_SPEED_DEC = ".-..-."

"""
/*  MORSE Code to set Mouse Speed to 1
 *  
 *  note : Write morse code between double quotes
 */
"""
MORSE_CODE_FOR_MOUSE_SPEED_1 = ".--.-."

"""
/*  MORSE Code to set Mouse Speed to 5
 *  
 *  note : Write morse code between double quotes
 */
"""
MORSE_CODE_FOR_MOUSE_SPEED_5 = ".--.--"

"""
/*  Lower limit for mouse speed set
 *  
 */
"""
MOUSE_SPEED_LOWER_LIMIT = 1

"""
/*  Upper limit for mouse speed set
 *  
 */
"""
MOUSE_SPEED_UPPER_LIMIT = 20

"""
/*  Mouse speed will be incremented/decremented 
 *  by this unit
 */
"""
MOUSE_SPEED_CHANGE_UNIT = 1

"""
/*  Serial Debug Enable/Disable
 *  1 - Enable / 0 - Disable
 *  
 *  By enabling device will send debug messages on USB port via serial. (Baudrate - 115200)
 */
"""
SERIAL_DEBUG_EN = 1

if ONE_BUTTON_MODE:    
    TWO_BUTTON_MODE = 0
    THREE_BUTTON_MODE = 0

if TWO_BUTTON_MODE:    
    ONE_BUTTON_MODE = 0
    THREE_BUTTON_MODE = 0

if THREE_BUTTON_MODE:    
    TWO_BUTTON_MODE = 0
    ONE_BUTTON_MODE = 0
