#ifndef MORSECODE_H_
#define MORSECODE_H_

#define MORSE_CODE_MAX_LENGTH     8

#define KEYBOARD_MODE     0
#define MOUSE_MODE        1

#define MOUSE_MOVE_RIGHT      0
#define MOUSE_MOVE_LEFT       1
#define MOUSE_MOVE_UP         2
#define MOUSE_MOVE_DOWN       3
#define MOUSE_CLICK_RIGHT     4
#define MOUSE_CLICK_LEFT      5
#define MOUSE_DB_CLICK_RIGHT  6
#define MOUSE_DB_CLICK_LEFT   7

void convertor(void);
const char findDotOrDash(void);
const char findDot(void);
const char findDash(void);
void handleConMouseMovement(void);         // v0.3
void handleSwitchControlKeypress(void);    // v0.3

#endif
