from adafruit_hid.keycode import Keycode

# keymap that translates predefined string characters into keycodes
from user.keymaps.us_keymap import keyboard_keymap

# printable keyboard characters
morseCodeKeyboard = {
  ".-"     : [Keycode.A],
  "-..."   : [Keycode.B],
  "---."   : [Keycode.C],
  "-.."    : [Keycode.D],
  "."      : [Keycode.E],
  "..-."   : [Keycode.F],
  "--."    : [Keycode.G],
  "...."   : [Keycode.H],
  ".."     : [Keycode.I],
  ".---"   : [Keycode.J],
  "-.-"    : [Keycode.K],
  ".-.."   : [Keycode.L],
  "--"     : [Keycode.M],
  "-."     : [Keycode.N],
  "---"    : [Keycode.O],
  ".--."   : [Keycode.P],
  "--.-"   : [Keycode.Q],
  ".-."    : [Keycode.R],
  "..."    : [Keycode.S],
  "-"      : [Keycode.T],
  "..-"    : [Keycode.U],
  "...-"   : [Keycode.V],
  ".--"    : [Keycode.W],
  "-..-"   : [Keycode.X],
  "-.--"   : [Keycode.Y],
  "--.."   : [Keycode.Z],
  "-----"  : [Keycode.ZERO],
  ".----"  : [Keycode.ONE],
  "..---"  : [Keycode.TWO],
  "...--"  : [Keycode.THREE],
  "....-"  : [Keycode.FOUR],
  "....."  : [Keycode.FIVE],
  "-...."  : [Keycode.SIX],
  "--..."  : [Keycode.SEVEN],
  "---.."  : [Keycode.EIGHT],
  "----."  : [Keycode.NINE],
  "----.." : [Keycode.BACKSLASH],
  "....--" : [Keycode.FORWARD_SLASH],
  ".--..." : [Keycode.LEFT_BRACKET],
  "-..---" : [Keycode.RIGHT_BRACKET],
  "--..--" : [Keycode.SHIFT, Keycode.COMMA],
  "..--.." : [Keycode.SHIFT, Keycode.PERIOD],
  "---..." : [Keycode.SHIFT, Keycode.NINE],
  "...---" : [Keycode.SHIFT, Keycode.ZERO],
  "..--."  : [Keycode.SHIFT, Keycode.LEFT_BRACKET],
  "--..-"  : [Keycode.SHIFT, Keycode.RIGHT_BRACKET],
  ".-----" : [Keycode.PERIOD],
  "-....." : [Keycode.COMMA],
  "----.-" : [Keycode.SHIFT, Keycode.MINUS],
  "....-." : [Keycode.SHIFT, Keycode.BACKSLASH],
  "-.----" : [Keycode.SHIFT, Keycode.FORWARD_SLASH],
  ".-...." : [Keycode.SHIFT, Keycode.ONE],
  "-....-" : [Keycode.SEMICOLON],
  ".----." : [Keycode.SHIFT, Keycode.SEMICOLON],
  ".---."  : [Keycode.MINUS],
  "..----" : [Keycode.SHIFT, Keycode.FOUR],
  "...-.-" : [Keycode.SHIFT, Keycode.FIVE],
  "...--." : [Keycode.SHIFT, Keycode.QUOTE],
  "---..-" : [Keycode.SHIFT, Keycode.TWO],
  "..-..." : [Keycode.QUOTE],
  "--.---" : [Keycode.GRAVE_ACCENT],
  "-...--" : [Keycode.SHIFT, Keycode.SIX],
  "---.--" : [Keycode.SHIFT, Keycode.GRAVE_ACCENT],
  "..---." : [Keycode.SHIFT, Keycode.THREE],
  ".---.." : [Keycode.SHIFT, Keycode.SEVEN],
  "-...-"  : [Keycode.SHIFT,Keycode.EQUALS],
  "---.-"  : [Keycode.EQUALS],
  "-..--"  : [Keycode.SHIFT, Keycode.EIGHT]
}

# non-printable keyboard characters
morseCodeKeyboard_special = {
  "..--"    : [Keycode.SPACEBAR],
  ".-.-"    : [Keycode.ENTER],
  ".-.--."  : [Keycode.BACKSPACE],
  "--...."  : [Keycode.ESCAPE],
  "--...-"  : [Keycode.SHIFT],
  "-.-."    : [Keycode.LEFT_CONTROL],
  "--.--"   : [Keycode.LEFT_ALT],
  ".-..-"   : [Keycode.UP_ARROW],
  ".--.."   : [Keycode.DOWN_ARROW],
  ".-.-.."  : [Keycode.LEFT_ARROW],
  ".-.-."   : [Keycode.RIGHT_ARROW],
  ".....-"  : [Keycode.PAGE_UP],
  "...-.."  : [Keycode.PAGE_DOWN],
  "......." : [Keycode.HOME],
  "...-..." : [Keycode.END],
  "---...-" : [Keycode.KEYPAD_NUMLOCK],
  "--.-.."  : [Keycode.SCROLL_LOCK],
  "-----."  : [Keycode.CAPS_LOCK],
  "-.-.."   : [Keycode.INSERT],
  "-.--.."  : [Keycode.DELETE],
  "--.--."  : [Keycode.PRINT_SCREEN],
  "---..-." : [Keycode.TAB],
  ".--.--"  : [Keycode.LEFT_GUI],
  "--.----" : [Keycode.F1 ],
  "--..---" : [Keycode.F2 ],
  "--...--" : [Keycode.F3 ],
  "--....-" : [Keycode.F4 ],
  "--....." : [Keycode.F5 ],
  "---...." : [Keycode.F6 ],
  "----..." : [Keycode.F7 ],
  "-----.." : [Keycode.F8 ],
  "------." : [Keycode.F9 ],
  "-------" : [Keycode.F10],
  ".------" : [Keycode.F11],
  "..-----" : [Keycode.F12],
}

# mouse commands
mouse_move_right       = "..."
mouse_move_left        = ".."
mouse_move_up          = "-"
mouse_move_down        = "--"
mouse_move_left_up     = ".--."
mouse_move_right_up    = "...-"
mouse_move_left_down   = "...--"
mouse_move_right_down  = "...---"
mouse_click_right      = ".--"
mouse_click_left       = ".-"
mouse_db_click_right   = "..--"
mouse_db_click_left    = "..-"
mouse_press_hold_right = "-.."
mouse_press_hold_left  = "-."
