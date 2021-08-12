#ifndef USERPINMAP_H_
#define USERPINMAP_H_

// Morse Button - 1
#define KEY_ONE			A0

// Morse Button - 2
#define KEY_TWO			A1

// Morse Button - 3
#define KEY_THREE		A2

// Switch for BLE connection Swapping
#define USER_SWITCH		A1

// Switch for Morse Mode & Switch Control Mode Swapping
#define USER_SWITCH2  A4     // v0.3b

// Buzzer for Morse code
#define BUZZER_PIN		13

// Hard Reset Pin
#define RESET_PIN     A5     // v0.3g // This should be D4 on itsybitsy but doesnt like it 

// NeoPixel LED
#define NEOPIXEL_PIN  PIN_NEOPIXEL     // v0.2
// Dotstar LED
#define DOTSTAR_CLOCK 6
#define DOTSTAR_DATA 8

#endif
