// Header Files
#include <string.h>
#include <bluefruit.h>
#include "morseCode.h"
#include "userConfig.h"

// Macros
#ifdef ONE_BUTTON_MODE
#undef TWO_BUTTON_MODE
#undef THREE_BUTTON_MODE
#endif

#ifdef TWO_BUTTON_MODE
#undef ONE_BUTTON_MODE
#undef THREE_BUTTON_MODE
#endif

#ifdef THREE_BUTTON_MODE
#undef TWO_BUTTON_MODE
#undef ONE_BUTTON_MODE
#endif

// Variable Declarations
extern BLEHidAdafruit blehid;
extern volatile uint32_t signal_len;
extern volatile char codeStr[MORSE_CODE_MAX_LENGTH];
extern volatile uint8_t hidMode;
extern int BUZZER;

const uint16_t dotLength = DOT_LENGTH;
const char DOT = '.';
const char DASH = '-';
const char keyMouseSwitchMorseCode[] = MORSE_CODE_FOR_KEYB_MOUSE_SWITCH;

struct MORSE
{
  char code[MORSE_CODE_MAX_LENGTH];
  int ch;
};

/*  Morse Codes reference : 
 *  https://www.makoa.org/jlubin/morsecode.htm
 */
const struct MORSE morseCodeKeyboard[] = {
  {".-",    'a'}, 
  {"-...",  'b'},
  {"---.",  'c'},
  {"-..",   'd'},
  {".",     'e'},
  {"..-.",  'f'},
  {"--.",   'g'},
  {"....",  'h'},
  {"..",    'i'},
  {".---",  'j'},
  {"-.-",   'k'},
  {".-..",  'l'},
  {"----",  'm'},
  {"-.",    'n'},
  {"---",   'o'},
  {".--.",  'p'},
  {"--.-",  'q'},
  {".-.",   'r'},
  {"...",   's'},
  {"-",     't'},
  {"..-",   'u'},
  {"...-",  'v'},
  {".--",   'w'},
  {"-..-",  'x'},
  {"-.--",  'y'},
  {"--..",  'z'},
  {"-----", '0'},
  {".----", '1'},
  {"..---", '2'},
  {"...--", '3'},
  {"....-", '4'},
  {".....", '5'},
  {"-....", '6'},
  {"--...", '7'},
  {"---..", '8'},
  {"----.", '9'},
  {"----..", '\\'},
  {"....--", '/'},
  {".--...", '['},
  {"-..---", ']'},
  {"--..--", '<'},
  {"..--..", '>'},
  {"---...", '('},
  {"...---", ')'},
  {"--..-",  '{'},
  {"--..-",  '}'},
  {".-----", '.'},
  {"-.....", ','},
  {"----.-", '_'},
  {"....-.", '|'},  
  {"-.----", '?'},  
  {".-....", '!'},
  {"-....-", ';'},
  {".----.", ':'},
  {".---.",  '-'},
  {"..----", '$'},
  {"...-.-", '%'},
  {"...--.", '"'},
  {"---..-", '@'},
  {"..-...", '\''},  
  {"--.---", '`'},
  {"-...--", '^'},
  {"---.--", '~'},
  {"..---.", '#'},
  {".---..", '&'},
  {"-...-",  '+'},  
  {"---.-",  '='},  
  {"-..--",  '*'},  
  {"..--",   32},         // Space
  {".-.-",   10},         // Enter           
  {"--",     8},          // Backspace
  {"--....", 27},         // ESC  
  {"--...-",  HID_KEY_SHIFT_LEFT + 255},       // Shift
  {"-.-.",    HID_KEY_CONTROL_LEFT + 255},     // Ctrl
  {"--.--",   HID_KEY_ALT_LEFT + 255},         // Alt
  {".-..-",   HID_KEY_ARROW_UP + 255},         // Arrow Up
  {".--..",   HID_KEY_ARROW_DOWN + 255},       // Arrow Down
  {".-.-..",  HID_KEY_ARROW_LEFT + 255},       // Arrow Left
  {".-.-.",   HID_KEY_ARROW_RIGHT + 255},      // Arrow Right
  {".....-",  HID_KEY_PAGE_UP + 255},          // Pg Up
  {"...-..",  HID_KEY_PAGE_DOWN + 255},        // Pg Dn
  {".......", HID_KEY_HOME + 255},             // Home
  {"...-...", HID_KEY_END + 255},              // End
  {"---...-", HID_KEY_NUM_LOCK + 255},         // Numlock
  {"--.-..",  HID_KEY_SCROLL_LOCK + 255},      // ScrollLock
  {"-----.",  HID_KEY_CAPS_LOCK + 255},        // Capslock
  {"-.-..",   HID_KEY_INSERT + 255},           // Insert
  {"-.--..",  HID_KEY_DELETE + 255},           // Delete
  {"--.--.",  HID_KEY_PRINT_SCREEN + 255},     // PrtScn
  {"---..-.", HID_KEY_TAB + 255},              // Tab
  {"--.----", HID_KEY_F1 + 255},               // F1
  {"--..---", HID_KEY_F2 + 255},               // F2
  {"--...--", HID_KEY_F3 + 255},               // F3
  {"--....-", HID_KEY_F4 + 255},               // F4
  {"--.....", HID_KEY_F5 + 255},               // F5
  {"---....", HID_KEY_F6 + 255},               // F6
  {"----...", HID_KEY_F7 + 255},               // F7
  {"-----..", HID_KEY_F8 + 255},               // F8
  {"------.", HID_KEY_F9 + 255},               // F9
  {"-------", HID_KEY_F10 + 255},              // F10
  {".------", HID_KEY_F11 + 255},              // F11
  {"..-----", HID_KEY_F12 + 255},              // F12
};

const struct MORSE morseCodeMouse[] = {
  {"...", MOUSE_MOVE_RIGHT},
  {"..",  MOUSE_MOVE_LEFT},
  {"-",   MOUSE_MOVE_UP},
  {"--",  MOUSE_MOVE_DOWN},
  {".--", MOUSE_CLICK_RIGHT},
  {".-",  MOUSE_CLICK_LEFT},
  {"..--",MOUSE_DB_CLICK_RIGHT},
  {"..-", MOUSE_DB_CLICK_LEFT}
};

// Functions Declarations
static void hidSpecialKeyPress(int keyType);
static void handleMouseMorseCode(void);

// Functions Definations
void convertor(void)
{
  static uint16_t i;

  i = 0;

  #if SERIAL_DEBUG_EN
  Serial.println(String((char*)codeStr));
  #endif

  if(!strcmp((const char*)codeStr, keyMouseSwitchMorseCode))
  {
    if(hidMode == KEYBOARD_MODE)
    {
      hidMode = MOUSE_MODE;
      #if SERIAL_DEBUG_EN
      Serial.println("MOUSE MODE");
      #endif
    }
    else
    {
      hidMode = KEYBOARD_MODE;
      #if SERIAL_DEBUG_EN
      Serial.println("KEYBOARD MODE");
      #endif
    }

    digitalWrite(BUZZER, LOW); delay(400);
    digitalWrite(BUZZER, HIGH);  delay(300);
    digitalWrite(BUZZER, LOW); delay(400);
    digitalWrite(BUZZER, HIGH);  delay(300);
    digitalWrite(BUZZER, LOW); delay(200);
    digitalWrite(BUZZER, HIGH);  delay(100);
    digitalWrite(BUZZER, LOW); delay(200);
    digitalWrite(BUZZER, HIGH);  delay(100);
  }
  else
  {
    if(hidMode == KEYBOARD_MODE)
    {
      for(i = 0; i < sizeof(morseCodeKeyboard); i++)
      {
        if(!strcmp((const char*)codeStr, morseCodeKeyboard[i].code))
        {
          if(morseCodeKeyboard[i].ch > 255)
          {
            hidSpecialKeyPress(morseCodeKeyboard[i].ch - 255);
          }
          else
          {
            #if SERIAL_DEBUG_EN
            Serial.print((char)morseCodeKeyboard[i].ch);
            #endif
            blehid.keyPress((char)morseCodeKeyboard[i].ch);
          }  
                             
          delay(50);
          blehid.keyRelease();
          break;
        }
      }

      if(i >= sizeof(morseCodeKeyboard))
      {
        #if SERIAL_DEBUG_EN
        Serial.println("<Wrong input>");
        #endif
      }
    }
    else
    {
      handleMouseMorseCode();
    }
  } 

  codeStr[0] = NULL;
  codeStr[1] = NULL;
  codeStr[2] = NULL;
  codeStr[3] = NULL;
  codeStr[4] = NULL;
  codeStr[5] = NULL;
  codeStr[6] = NULL;
  codeStr[7] = NULL;
  //memset((char*)codeStr, '\0', sizeof((char*)codeStr));  
}

static void hidSpecialKeyPress(int keyType)
{
  hid_keyboard_report_t report;
  varclr(&report);

  report.modifier = 0;
  report.keycode[0] = keyType;

  blehid.keyboardReport(BLE_CONN_HANDLE_INVALID, &report);
}

static void handleMouseMorseCode(void)
{
  if(!strcmp((const char*)codeStr, morseCodeMouse[MOUSE_MOVE_RIGHT].code))
  {
    blehid.mouseMove(MOUSE_MOVE_STEP, 0);
  }
  else if(!strcmp((const char*)codeStr, morseCodeMouse[MOUSE_MOVE_LEFT].code))
  {
    blehid.mouseMove(-MOUSE_MOVE_STEP, 0);
  }
  else if(!strcmp((const char*)codeStr, morseCodeMouse[MOUSE_MOVE_UP].code))
  {
    blehid.mouseMove(0, -MOUSE_MOVE_STEP);
  }
  else if(!strcmp((const char*)codeStr, morseCodeMouse[MOUSE_MOVE_DOWN].code))
  {
    blehid.mouseMove(0, MOUSE_MOVE_STEP);
  }
  else if(!strcmp((const char*)codeStr, morseCodeMouse[MOUSE_CLICK_RIGHT].code))
  {
    blehid.mouseButtonPress(MOUSE_BUTTON_RIGHT);
    delay(50);
    blehid.mouseButtonRelease();
  }
  else if(!strcmp((const char*)codeStr, morseCodeMouse[MOUSE_CLICK_LEFT].code))
  {
    blehid.mouseButtonPress(MOUSE_BUTTON_LEFT);
    delay(50);
    blehid.mouseButtonRelease();
  }
  else if(!strcmp((const char*)codeStr, morseCodeMouse[MOUSE_DB_CLICK_RIGHT].code))
  {
    blehid.mouseButtonPress(MOUSE_BUTTON_RIGHT);
    delay(50);
    blehid.mouseButtonRelease();
    blehid.mouseButtonPress(MOUSE_BUTTON_RIGHT);
    delay(50);
    blehid.mouseButtonRelease();
  }
  else if(!strcmp((const char*)codeStr, morseCodeMouse[MOUSE_DB_CLICK_LEFT].code))
  {
    blehid.mouseButtonPress(MOUSE_BUTTON_LEFT);
    delay(50);
    blehid.mouseButtonRelease();
    blehid.mouseButtonPress(MOUSE_BUTTON_LEFT);
    delay(50);
    blehid.mouseButtonRelease();
  }
  else
  {
    #if SERIAL_DEBUG_EN
    Serial.println("<Wrong Input>");
    #endif
  }
}

const char findDotOrDash(void)
{
  if(signal_len <= dotLength)
  {
    return DOT;
  }
  else
  {
    return DASH;
  }
}

const char findDot(void)
{
  if(signal_len <= dotLength)
  {
    return DOT;
  }
  else
  {
    return NULL;
  }
}

const char findDash(void)
{
  if(signal_len <= dotLength)
  {
    return NULL;
  }
  else
  {
    return DASH;
  }
}
