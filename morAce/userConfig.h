#ifndef USERCONFIG_H_
#define USERCONFIG_H_

/*  Device Specific Settings
 *  DEVICE_BLE_NAME     : Device will advertise by this name in Morse Mode
 *  DEVICE_BLE_NAME2    : Device will advertise by this name in Switch Control Mode
 *  DEVICE_MANUFACTURER : Manufacturere name in BLE device properties
 *  DEVICE_MODEL_NAME   : Modem name in BLE device properties
 *  
 *  note - Write string between double quotes
 */
#define DEVICE_BLE_NAME         "MORSE_HID"
#define DEVICE_BLE_NAME2        "SW_HID"                // v0.3c
#define DEVICE_MANUFACTURER     "AceCentre"
#define DEVICE_MODEL_NAME       "BLE-HID-v1"

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
#define ONE_BUTTON_MODE

/*  Fast Typing Mode Enable/Disable 
 *  Effective only in Two & Three Button Modes
 *  When Enable, by pressing down a button, device will accept multiple Dots/Dashes depending on press time
 *  
 *  1 - Enable / 0 - Disable
 */
#define FAST_TYPING_MODE        0

/*  MORSE Code Settings 
 *  DOT_LENGTH : Unit length of a dot in tearms of milliseconds
 */
#define DOT_LENGTH              200

/*  MORSE Code for switching between Keyboard mode and Mouse mode
 *  
 *  note : Write morse code between double quotes
 */
#define MORSE_CODE_FOR_KEYB_MOUSE_SWITCH      ".-.--"

/*  MORSE Code for Swap Connection
 *  
 *  note : Write morse code between double quotes
 */
#define MORSE_CODE_FOR_BLE_SWAP_CONNECTION     "-.-.--"         // v0.3

/*  Define timeout for BLE connection swapping
 *  By pressing a switch to swap BLE connection, if device is not connected to another PC till this timeout,
 *  then device will reconnect with older PC.
 *  
 *  note : Define timeout in milliseconds
 */
#define LAST_CONNECTION_CHECK_TIMEOUT          10000

/*  Mouse HID - Step size for Mouse movement
 *  Mouse cursor will be moved by this step size
 *  
 *  note : Step must be integer
 */
#define MOUSE_MOVE_STEP                5

/*  Time interval to send mouse movement command in milliseconds
 *  Mouse move command to right/left/up/down will be sent at this interval
 *  
 *  note : Define timeout in milliseconds
 */
#define INTERVAL_SEND_MOUSE_MOVE_CMD   100              // v0.3

/*  Maximum allowable BLE connections swaps
 *  
 *  note : Must be <= 5
 */ 
#define MAXIMUM_SWAP_CONNECTIONS       4                // v0.3c

/*  Serial Debug Enable/Disable
 *  1 - Enable / 0 - Disable
 *  
 *  By enabling device will send debug messages on USB port via serial. (Baudrate - 115200)
 */
#define SERIAL_DEBUG_EN                0


#endif
