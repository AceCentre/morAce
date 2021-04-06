#ifndef MORSECODE_H_
#define MORSECODE_H_

#define MORSE_CODE_MAX_LENGTH     13      // 8      // v0.3e

// Device Mode
#define KEYBOARD_MODE     0
#define MOUSE_MODE        1

// Mouse Commands                          // v0.3e - Revised numbering
#define MOUSE_MOVE_RIGHT        1
#define MOUSE_MOVE_LEFT         2
#define MOUSE_MOVE_UP           3
#define MOUSE_MOVE_DOWN         4
#define MOUSE_MOVE_LEFT_UP      5          // v0.3e
#define MOUSE_MOVE_RIGHT_UP     6          // v0.3e
#define MOUSE_MOVE_LEFT_DOWN    7          // v0.3e
#define MOUSE_MOVE_RIGHT_DOWN   8          // v0.3e
#define MOUSE_CLICK_RIGHT       9
#define MOUSE_CLICK_LEFT        10
#define MOUSE_DB_CLICK_RIGHT    11
#define MOUSE_DB_CLICK_LEFT     12

// Shortcut Commands                       // v0.3e
#define SHORTCUT_CTRL_C       0
#define SHORTCUT_CTRL_V       1
#define SHORTCUT_WIN_TAB      2
#define SHORTCUT_WIN_H        3

// Type of last sent command              // v0.3e
#define REG_KEYBOARD_CHAR     0
#define SPL_KEYBOARD_CHAR     1
#define MOUSE_CMD             2

// Type of Output                         // v0.3f
#define ACTIVE_HIGH           0
#define ACTIVE_LOW            1

// Type of Buzzer                         // v0.3f
#define BUZZER_TYPE           ACTIVE_HIGH

void convertor(void);
const char findDotOrDash(void);
const char findDot(void);
const char findDash(void);
void handleConMouseMovement(void);         // v0.3
void handleSwitchControlKeypress(void);    // v0.3
void handleRepeatCmdAction(void);          // v0.3e

#endif
