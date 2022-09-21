from adafruit_hid.keycode import Keycode

# keymap that translates predefined string characters into keycodes
from user.keymaps.us_keymap import keyboard_keymap

# printable keyboard characters
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
  ("--",    [Keycode.M]),
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
  ("..--.",  [Keycode.SHIFT, Keycode.LEFT_BRACKET]),
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

# non-rintable keyboard characters
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

# mouse commands
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
    ("-..",    mouse_press_hold_right),
    ("-.",     mouse_press_hold_left)
]