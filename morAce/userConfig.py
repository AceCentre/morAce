
x80_pinout = True # True if x80 board is used

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
device_ble_name = "MORSE_HID"
device_ble_name2 = "SW_HID"                #// v0.3c
device_manufacturer = "ABC"
device_model_name = "BLE-HID-v1"

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
one_button_mode = 1
two_button_mode = 0
three_button_mode = 0


morse_mode = 0
sw_ctrl_mode = 1
"""
/*  Fast Typing Mode Enable/Disable 
 *  Effective only in Two & Three Button Modes
 *  When Enable, by pressing down a button, device will accept multiple Dots/Dashes depending on press time
 *  
 *  1 - Enable / 0 - Disable
 */
"""
fast_typing_mode = 0

"""
/*  MORSE Code Settings 
 *  DOT_LENGTH : Unit length of a dot in tearms of milliseconds
 */
"""
dot_length = 200

"""
/*  MORSE Code for switching between Keyboard mode and Mouse mode
 *  
 *  note : Write morse code between double quotes
 */
"""
keyMouseSwitchMorseCode = ".-.--"

"""
/*  Default mode for the device : Keyboard Mode / Mouse Mode
 *  
 *  For Keyboard Mode : KEYBOARD_MODE
 *  For Mouse Mode    : MOUSE_MODE
 */
"""
keyboard_mode = 0
mouse_mode = 1

default_mode_of_device = mouse_mode

"""
/*  MORSE Code for Swap Connection
 *  
 *  note : Write morse code between double quotes
 */
"""
swapBleConnectionMorseCode  = "-.-.--"

"""
/*  Define timeout for BLE connection swapping
 *  By pressing a switch to swap BLE connection, if device is not connected to another PC till this timeout,
 *  then device will reconnect with older PC.
 *  
 *  note : Define timeout in milliseconds
 */
"""
last_connection_check_timeout = 10000

"""
/*  Mouse HID - Default Step size for Mouse movement
 *  Mouse cursor will be moved by this step size (If not set by user)
 *  
 *  note : Step must be integer
 */
"""
default_mouse_move_step = 5

"""
/*  Maximum allowable BLE connections swaps
 *  
 *  note : Must be <= 5
 */ 
"""

maxSwapConn = 4

"""
/*  MORSE Code for REPEAT Command
 *  Previous Morse command (Keyboard Character/Mouse Commands) 
 *  will be repeated after sending this REPEAT command morse code
 *  note : Write morse code between double quotes
 */
"""
repeatCmdMorseCode = ".---.-"

"""
/*  MORSE Code for HOLD Command
 *  Send this command first to hold down any key/mouse click
 *  and then after send command for key/mouse clik you want to hold
 *  note : Write morse code between double quotes
 */
"""
holdCmdMorseCode = ".---.-."

"""
/*  MORSE Code for RELEASE Command
 *  Send this command to release prevoiusly holded key/mouse click
 *  note : Write morse code between double quotes
 */
"""
releaseCmdMorseCode = ".---.--"

"""
/*  Time interval to send REPEAT command in milliseconds
 *  Previous Morse command (Keyboard Character/Mouse Commands)
 *  will be sent at this interval
 *  note : Define timeout in milliseconds
 */
"""
interval_send_repeat_cmd = 100

"""
/*  MORSE Code for Mouse Speed Increase
 *  
 *  note : Write morse code between double quotes
 */
"""

mouseSpeedIncMorseCode = ".-..--"

"""
/*  MORSE Code for Mouse Speed Decrease
 *  
 *  note : Write morse code between double quotes
 */
"""

mouseSpeedDecMorseCode = ".-..-."

"""
/*  MORSE Code to set Mouse Speed to 1
 *  
 *  note : Write morse code between double quotes
 */
"""
mouseSpeedSet1MorseCode = ".--.-."

"""
/*  MORSE Code to set Mouse Speed to 5
 *  
 *  note : Write morse code between double quotes
 */
"""
mouseSpeedSet5MorseCode = ".--.--"

"""
/*  Lower limit for mouse speed set
 *  
 */
"""
mouse_speed_lower_limit = 1

"""
/*  Upper limit for mouse speed set
 *  
 */
"""
mouse_speed_upper_limit = 20

"""
/*  Mouse speed will be incremented/decremented 
 *  by this unit
 */
"""
mouse_speed_change_unit = 1

"""
/*  Serial Debug Enable/Disable
 *  1 - Enable / 0 - Disable
 *  
 *  By enabling device will send debug messages on USB port via serial. (Baudrate - 115200)
 */
"""
serial_debug_en = 1

# Dot and dash constants
dot = '.'
dash = '-'

# Buzzer type
active_high = 0
active_low  = 1

buzzer_type = active_high

# Max length of morse buffer
morse_code_max_length = 13
