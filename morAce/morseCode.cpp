// Header Files
#include <string.h>
#include <bluefruit.h>
#include "morseCode.h"
#include "userConfig.h"
#include "userPinMap.h"

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
const int BUTTON_ONE = KEY_ONE;
const int BUTTON_TWO = KEY_TWO;
const int BUTTON_THREE = KEY_THREE;
extern BLEHidAdafruit blehid;
extern volatile uint32_t signal_len;
extern volatile char codeStr[MORSE_CODE_MAX_LENGTH];
extern volatile uint8_t hidMode;
extern int BUZZER;
extern volatile uint8_t flag_mouseConMovement;     // v0.3
extern volatile uint8_t flag_repeatCmdEnable;      // v0.3e
extern volatile uint8_t mouseMoveStep;             // v0.3e

const uint16_t dotLength = DOT_LENGTH;
const char DOT = '.';
const char DASH = '-';
const char keyMouseSwitchMorseCode[] = MORSE_CODE_FOR_KEYB_MOUSE_SWITCH;
const char swapBleConnectionMorseCode[] = MORSE_CODE_FOR_BLE_SWAP_CONNECTION;   // v0.3
const char repeatCmdMorseCode[] = MORSE_CODE_FOR_REPEAT_CMD;                    // v0.3e
const char mouseSpeedIncMorseCode[] = MORSE_CODE_FOR_MOUSE_SPEED_INC;           // v0.3e
const char mouseSpeedDecMorseCode[] = MORSE_CODE_FOR_MOUSE_SPEED_DEC;           // v0.3e
const char mouseSpeedSet1MorseCode[] = MORSE_CODE_FOR_MOUSE_SPEED_1;            // v0.3e
const char mouseSpeedSet5MorseCode[] = MORSE_CODE_FOR_MOUSE_SPEED_5;            // v0.3e
const char holdCmdMorseCode[] = MORSE_CODE_FOR_HOLD_CMD;                        // v0.3e
const char releaseCmdMorseCode[] = MORSE_CODE_FOR_RELEASE_CMD;                  // v0.3e
volatile uint8_t keycheck;
volatile uint8_t keycodeComboBuff[6];             // v0.3e
volatile int lastKeyboardChar;                    // v0.3e
volatile uint8_t lastSentCmdType;                 // v0.3e 
volatile uint8_t flag_hold, flag_release;         // v0.3e

struct MORSE
{
  char code[MORSE_CODE_MAX_LENGTH];
  int ch;
};

struct MORSE_STR                      // v0.3e
{
  char code[MORSE_CODE_MAX_LENGTH];
  char predefinedStr[50];
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
  {"..--",    HID_KEY_SPACE + 255},            // Space
  {".-.-",    HID_KEY_RETURN + 255},           // Enter           
  {".-.--.",  HID_KEY_BACKSPACE + 255},        // Backspace         // v0.3e - changed morse code (older same with mouse down)
  {"--....",  HID_KEY_ESCAPE + 255},           // ESC  
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
  {NULL,    0},                           // v0.3e - Just for logic adjustment
  {"...",   MOUSE_MOVE_RIGHT},
  {"..",    MOUSE_MOVE_LEFT},
  {"-",     MOUSE_MOVE_UP},
  {"--",    MOUSE_MOVE_DOWN},
  {".--.",  MOUSE_MOVE_LEFT_UP},          // v0.3e
  {"...-",  MOUSE_MOVE_RIGHT_UP},         // v0.3e
  {"...--", MOUSE_MOVE_LEFT_DOWN},        // v0.3e
  {"...---", MOUSE_MOVE_RIGHT_DOWN},      // v0.3e
  {".--",   MOUSE_CLICK_RIGHT},
  {".-",    MOUSE_CLICK_LEFT},
  {"..--",  MOUSE_DB_CLICK_RIGHT},
  {"..-",   MOUSE_DB_CLICK_LEFT}
};

const struct MORSE_STR morseCodePredefinedStr[] = {               // v0.3e
  {"---...-.",      "My name is Morace"},
  {"-..--.",        "No problem"},
  {"-..---.",       "Thank you"},
  {"-.-...--.-..",  "See you later"},
  {"..--..---..",   "How are you?"}
};

const struct MORSE morseCodeShortcutCmd[] = {                     // v0.3e
  {"....----", SHORTCUT_CTRL_C},
  {"...-----", SHORTCUT_CTRL_V},
  {"..--.",    SHORTCUT_WIN_TAB},
  {"..-....",  SHORTCUT_WIN_H}
};

// Functions Declarations
void hidSpecialKeyPress(uint8_t buff[6]);                         // v0.3e
static void handleMouseMorseCode(void);
extern void handleBleConnectionSwap(void);                        // v0.3
extern void writeDataToFS(void);                                  // v0.3e
static uint8_t checkPredefinedStrings(void);                      // v0.3e
static uint8_t checkShortcutCommands(void);                       // v0.3e
static uint8_t checkSpecialKey(void);                             // v0.3e

// Functions Definations
void convertor(void)
{
  static uint16_t i;

  i = 0; 

  #if SERIAL_DEBUG_EN
  Serial.println();
  Serial.print("Morse Buffer: ");
  Serial.println(String((char*)codeStr));
  #endif

  if(flag_repeatCmdEnable)           // v0.3e
  {
    flag_repeatCmdEnable = 0;
  }
  else if(!strcmp((const char*)codeStr, keyMouseSwitchMorseCode))
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
    
    // Write updated data into FS
    writeDataToFS();                              // v0.3e
    
    digitalWrite(BUZZER, HIGH); delay(400);       // v0.3f
    digitalWrite(BUZZER, LOW);  delay(300);
    digitalWrite(BUZZER, HIGH); delay(400);
    digitalWrite(BUZZER, LOW);  delay(300);
    digitalWrite(BUZZER, HIGH); delay(200);
    digitalWrite(BUZZER, LOW);  delay(100);
    digitalWrite(BUZZER, HIGH); delay(200);
    digitalWrite(BUZZER, LOW);  delay(100);
  }
  else if(!strcmp((const char*)codeStr, swapBleConnectionMorseCode))      // v0.3
  {
    handleBleConnectionSwap();
  }
  else if(!strcmp((const char*)codeStr, repeatCmdMorseCode))              // v0.3e
  {
    flag_repeatCmdEnable = 1;
    #if SERIAL_DEBUG_EN
    Serial.print("REPEAT CMD");
    #endif
  }
  else if(!strcmp((const char*)codeStr, mouseSpeedIncMorseCode))          // v0.3e
  {
    mouseMoveStep += MOUSE_SPEED_CHANGE_UNIT;
    if(mouseMoveStep > MOUSE_SPEED_UPPER_LIMIT)
    {
      mouseMoveStep = MOUSE_SPEED_UPPER_LIMIT;
    }
    
    // Write updated data into FS
    writeDataToFS();
    
    #if SERIAL_DEBUG_EN
    Serial.print("Mouse Speed Inc, New: " + String(mouseMoveStep));
    #endif
  }
  else if(!strcmp((const char*)codeStr, mouseSpeedDecMorseCode))          // v0.3e
  {
    mouseMoveStep -= MOUSE_SPEED_CHANGE_UNIT;
    if(mouseMoveStep < MOUSE_SPEED_LOWER_LIMIT || mouseMoveStep > MOUSE_SPEED_UPPER_LIMIT)
    {
      mouseMoveStep = MOUSE_SPEED_LOWER_LIMIT;
    }

    // Write updated data into FS
    writeDataToFS();
        
    #if SERIAL_DEBUG_EN
    Serial.print("Mouse Speed Dec, New: " + String(mouseMoveStep));
    #endif
  }
  else if(!strcmp((const char*)codeStr, mouseSpeedSet1MorseCode))          // v0.3e
  {
    mouseMoveStep = 1;

    // Write updated data into FS
    writeDataToFS();
        
    #if SERIAL_DEBUG_EN
    Serial.print("Mouse Speed Set to 1, New: " + String(mouseMoveStep));
    #endif
  }
  else if(!strcmp((const char*)codeStr, mouseSpeedSet5MorseCode))          // v0.3e
  {
    mouseMoveStep = 5;

    // Write updated data into FS
    writeDataToFS();
    
    #if SERIAL_DEBUG_EN
    Serial.print("Mouse Speed Set to 5, New: " + String(mouseMoveStep));
    #endif
  }
  else if(!strcmp((const char*)codeStr, holdCmdMorseCode))                 // v0.3e
  {
    flag_hold = 1;
    flag_release = 0;
    #if SERIAL_DEBUG_EN
    Serial.print("Cmd: Hold");
    #endif
  }
  else if(!strcmp((const char*)codeStr, releaseCmdMorseCode))              // v0.3e
  {
    if(flag_hold)
    {
      blehid.mouseButtonRelease();
      flag_hold = 0;
      #if SERIAL_DEBUG_EN
      Serial.print("Cmd: Release");
      #endif
    }    
    else
    {
      #if SERIAL_DEBUG_EN
      Serial.print("Release Cmd Error");
      #endif
    }
  }
  else
  {
    if(checkPredefinedStrings())             // v0.3e
    {
      
    }
    else if(checkShortcutCommands())         // v0.3e
    {
      
    }
    else if(checkSpecialKey())               // v0.3e
    {
      
    }
    else if(hidMode == KEYBOARD_MODE)
    {
      for(i = 0; i < 68; i++)               // v0.3e
      {
        if(!strcmp((const char*)codeStr, morseCodeKeyboard[i].code))
        {          
          #if SERIAL_DEBUG_EN
          Serial.print("Char: " + String((char)morseCodeKeyboard[i].ch));
          #endif
          blehid.keyPress((char)morseCodeKeyboard[i].ch);
          delay(20);
          lastSentCmdType = REG_KEYBOARD_CHAR;                                // v0.3e
          lastKeyboardChar = (char)morseCodeKeyboard[i].ch;                   // v0.3e
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

  for(int i = 0; i < sizeof(codeStr); i++)        // v0.3e
  {
    codeStr[i] = NULL;
  }   
}

void hidSpecialKeyPress(uint8_t buff[6])           // v0.3e
{
  hid_keyboard_report_t report;
  varclr(&report);

  report.modifier = 0;
  report.keycode[0] = buff[0];
  report.keycode[1] = buff[1];
  report.keycode[2] = buff[2];
  report.keycode[3] = buff[3];
  report.keycode[4] = buff[4];
  report.keycode[5] = buff[5];

  blehid.keyboardReport(BLE_CONN_HANDLE_INVALID, &report);
  delay(20);
  blehid.keyRelease();
  
  memset((uint8_t*)keycodeComboBuff, NULL, sizeof(keycodeComboBuff));
}

static void handleMouseMorseCode(void)
{
  /*if(flag_mouseConMovement)           // v0.3
  {
    flag_mouseConMovement = 0;
  }
  else
  {*/   // Commented in v0.3e
    if(!strcmp((const char*)codeStr, morseCodeMouse[MOUSE_MOVE_RIGHT].code))
    {
      lastSentCmdType = MOUSE_CMD;              // v0.3e
      flag_mouseConMovement = MOUSE_MOVE_RIGHT; // v0.3
      blehid.mouseMove(mouseMoveStep, 0);
      #if SERIAL_DEBUG_EN
      Serial.println("Mouse: Right");
      #endif
    }
    else if(!strcmp((const char*)codeStr, morseCodeMouse[MOUSE_MOVE_LEFT].code))
    {
      lastSentCmdType = MOUSE_CMD;              // v0.3e
      flag_mouseConMovement = MOUSE_MOVE_LEFT;  // v0.3
      blehid.mouseMove(-mouseMoveStep, 0);
      #if SERIAL_DEBUG_EN
      Serial.println("Mouse: Left");
      #endif
    }
    else if(!strcmp((const char*)codeStr, morseCodeMouse[MOUSE_MOVE_UP].code))
    {
      lastSentCmdType = MOUSE_CMD;              // v0.3e
      flag_mouseConMovement = MOUSE_MOVE_UP;    // v0.3
      blehid.mouseMove(0, -mouseMoveStep);
      #if SERIAL_DEBUG_EN
      Serial.println("Mouse: Up");
      #endif
    }
    else if(!strcmp((const char*)codeStr, morseCodeMouse[MOUSE_MOVE_DOWN].code))
    {
      lastSentCmdType = MOUSE_CMD;              // v0.3e
      flag_mouseConMovement = MOUSE_MOVE_DOWN;  // v0.3      
      blehid.mouseMove(0, mouseMoveStep);
      #if SERIAL_DEBUG_EN
      Serial.println("Mouse: Down");
      #endif
    }
    else if(!strcmp((const char*)codeStr, morseCodeMouse[MOUSE_MOVE_LEFT_UP].code))     // v0.3e
    {
      lastSentCmdType = MOUSE_CMD;
      flag_mouseConMovement = MOUSE_MOVE_LEFT_UP;
      blehid.mouseMove(-mouseMoveStep, -mouseMoveStep);
      #if SERIAL_DEBUG_EN
      Serial.println("Mouse: Left-Up");
      #endif
    }
    else if(!strcmp((const char*)codeStr, morseCodeMouse[MOUSE_MOVE_RIGHT_UP].code))     // v0.3e
    {
      lastSentCmdType = MOUSE_CMD;
      flag_mouseConMovement = MOUSE_MOVE_RIGHT_UP;
      blehid.mouseMove(mouseMoveStep, -mouseMoveStep);
      #if SERIAL_DEBUG_EN
      Serial.println("Mouse: Right-Up");
      #endif
    }
    else if(!strcmp((const char*)codeStr, morseCodeMouse[MOUSE_MOVE_LEFT_DOWN].code))     // v0.3e
    {
      lastSentCmdType = MOUSE_CMD;
      flag_mouseConMovement = MOUSE_MOVE_LEFT_DOWN;
      blehid.mouseMove(-mouseMoveStep, mouseMoveStep);
      #if SERIAL_DEBUG_EN
      Serial.println("Mouse: Left-Down");
      #endif
    }
    else if(!strcmp((const char*)codeStr, morseCodeMouse[MOUSE_MOVE_RIGHT_DOWN].code))     // v0.3e
    {
      lastSentCmdType = MOUSE_CMD;
      flag_mouseConMovement = MOUSE_MOVE_RIGHT_DOWN;
      blehid.mouseMove(mouseMoveStep, mouseMoveStep);
      #if SERIAL_DEBUG_EN
      Serial.println("Mouse: Right-Down");
      #endif
    }
    else if(!strcmp((const char*)codeStr, morseCodeMouse[MOUSE_CLICK_RIGHT].code))
    {
      blehid.mouseButtonPress(MOUSE_BUTTON_RIGHT);
      if(!flag_hold)                                    // v0.3e
      {
        delay(20);
        blehid.mouseButtonRelease();
      }      
      #if SERIAL_DEBUG_EN
      Serial.print("Mouse: Right Click");
      #endif
    }
    else if(!strcmp((const char*)codeStr, morseCodeMouse[MOUSE_CLICK_LEFT].code))
    {
      blehid.mouseButtonPress(MOUSE_BUTTON_LEFT);
      if(!flag_hold)                                    // v0.3e
      {
        delay(20);
        blehid.mouseButtonRelease();
      } 
      #if SERIAL_DEBUG_EN
      Serial.print("Mouse: Left Click");
      #endif
    }
    else if(!strcmp((const char*)codeStr, morseCodeMouse[MOUSE_DB_CLICK_RIGHT].code))
    {
      blehid.mouseButtonPress(MOUSE_BUTTON_RIGHT);
      delay(50);
      blehid.mouseButtonRelease();
      blehid.mouseButtonPress(MOUSE_BUTTON_RIGHT);
      delay(50);
      blehid.mouseButtonRelease();
      #if SERIAL_DEBUG_EN
      Serial.print("Mouse: Right Double Click");
      #endif
    }
    else if(!strcmp((const char*)codeStr, morseCodeMouse[MOUSE_DB_CLICK_LEFT].code))
    {
      blehid.mouseButtonPress(MOUSE_BUTTON_LEFT);
      delay(50);
      blehid.mouseButtonRelease();
      blehid.mouseButtonPress(MOUSE_BUTTON_LEFT);
      delay(50);
      blehid.mouseButtonRelease();
      #if SERIAL_DEBUG_EN
      Serial.print("Mouse: Left Double Click");
      #endif
    }
    else
    {
      #if SERIAL_DEBUG_EN
      Serial.println("<Wrong Input>");
      #endif
    }
  //}   // Commented in v0.3e
  
}

static uint8_t checkPredefinedStrings(void)                    // v0.3e
{  
  static uint16_t j;
  
  for(j = 0; j < (sizeof(morseCodePredefinedStr) / sizeof(morseCodePredefinedStr[0])); j++)
  {
    if(!strcmp((const char*)codeStr, morseCodePredefinedStr[j].code))
    {
      #if SERIAL_DEBUG_EN      
      Serial.print("Predfined Str: ");
      Serial.println(morseCodePredefinedStr[j].predefinedStr);
      #endif
      for(uint8_t k = 0; k < strlen(morseCodePredefinedStr[j].predefinedStr); k++)
      {
        blehid.keyPress((char)morseCodePredefinedStr[j].predefinedStr[k]);
        delay(20);
        blehid.keyRelease();
      }
      return 1;
    }
  }
  
  return 0;
}

static uint8_t checkShortcutCommands(void)                       // v0.3e
{
  if(!strcmp((const char*)codeStr, morseCodeShortcutCmd[SHORTCUT_CTRL_C].code))
  {
    #if SERIAL_DEBUG_EN      
    Serial.print("Shortcut Cmd: CTRL+C");
    #endif  
    
    keycodeComboBuff[0] = HID_KEY_CONTROL_LEFT;
    keycodeComboBuff[1] = HID_KEY_C;
    hidSpecialKeyPress((uint8_t*)keycodeComboBuff);
  }
  else if(!strcmp((const char*)codeStr, morseCodeShortcutCmd[SHORTCUT_CTRL_V].code))
  {
    #if SERIAL_DEBUG_EN      
    Serial.print("Shortcut Cmd: CTRL+V");
    #endif
    
    keycodeComboBuff[0] = HID_KEY_CONTROL_LEFT;
    keycodeComboBuff[1] = HID_KEY_V;
    hidSpecialKeyPress((uint8_t*)keycodeComboBuff);
  }
  else if(!strcmp((const char*)codeStr, morseCodeShortcutCmd[SHORTCUT_WIN_TAB].code))
  {
    #if SERIAL_DEBUG_EN      
    Serial.print("Shortcut Cmd: WIN+TAB");
    #endif
    
    keycodeComboBuff[0] = HID_KEY_GUI_LEFT;
    keycodeComboBuff[1] = HID_KEY_TAB;
    hidSpecialKeyPress((uint8_t*)keycodeComboBuff);
  }
  else if(!strcmp((const char*)codeStr, morseCodeShortcutCmd[SHORTCUT_WIN_H].code))
  {
    #if SERIAL_DEBUG_EN      
    Serial.print("Shortcut Cmd: WIN+H");
    #endif
    
    keycodeComboBuff[0] = HID_KEY_GUI_LEFT;
    keycodeComboBuff[1] = HID_KEY_H;
    hidSpecialKeyPress((uint8_t*)keycodeComboBuff);
  }
  else
  {
    return 0;
  }

  return 1;  
}

static uint8_t checkSpecialKey(void)                             // v0.3e
{
  static uint16_t i;
  
  for(i = 68; i < (sizeof(morseCodeKeyboard) / sizeof(morseCodeKeyboard[0])); i++)
  {
    if(!strcmp((const char*)codeStr, morseCodeKeyboard[i].code))
    {
      if(morseCodeKeyboard[i].ch > 255)
      {    
        keycodeComboBuff[0] = morseCodeKeyboard[i].ch - 255;
        lastSentCmdType = SPL_KEYBOARD_CHAR;
        lastKeyboardChar = keycodeComboBuff[0];
        hidSpecialKeyPress((uint8_t*)keycodeComboBuff);        
      }
      else{}
      return 1;
    }
  }
  return 0;
}

void handleSwitchControlKeypress(void)                          // v0.3
{
  #ifdef ONE_BUTTON_MODE
    if(digitalRead(BUTTON_ONE) == LOW)
    {
      if(keycheck)
      {
        digitalWrite(BUZZER, HIGH);     // v0.3f
        keycheck = 0;
        blehid.keyPress((char)32);                       
        delay(50);
        blehid.keyRelease();
        digitalWrite(BUZZER, LOW);      // v0.3f
      }
    }
    else 
    {
      keycheck = 1;
    }
  #endif

  #ifdef TWO_BUTTON_MODE
    if(digitalRead(BUTTON_ONE) == LOW)
    {
      if(keycheck)
      {
        digitalWrite(BUZZER, HIGH);     // v0.3f
        keycheck = 0;
        blehid.keyPress((char)32);                       
        delay(50);
        blehid.keyRelease();
        digitalWrite(BUZZER, LOW);      // v0.3f
      }
    }
    else if(digitalRead(BUTTON_TWO) == LOW)
    {
      if(keycheck)
      {
        digitalWrite(BUZZER, HIGH);     // v0.3f
        keycheck = 0;
        blehid.keyPress((char)10);                       
        delay(50);
        blehid.keyRelease();
        digitalWrite(BUZZER, LOW);      // v0.3f
      }
    }
    else 
    {
      keycheck = 1;
    }
  #endif

  #ifdef THREE_BUTTON_MODE
    if(digitalRead(BUTTON_ONE) == LOW)
    {
      if(keycheck)
      {
        digitalWrite(BUZZER, HIGH);     // v0.3f
        keycheck = 0;
        blehid.keyPress((char)32);                       
        delay(50);
        blehid.keyRelease();
        digitalWrite(BUZZER, LOW);      // v0.3f
      }
    }
    else if(digitalRead(BUTTON_TWO) == LOW)
    {
      if(keycheck)
      {
        digitalWrite(BUZZER, HIGH);     // v0.3f
        keycheck = 0;
        blehid.keyPress((char)10);                       
        delay(50);
        blehid.keyRelease();
        digitalWrite(BUZZER, LOW);      // v0.3f
      }
    }
    else if(digitalRead(BUTTON_THREE) == LOW)
    {
      if(keycheck)
      {
        digitalWrite(BUZZER, HIGH);     // v0.3f
        keycheck = 0;
        blehid.keyPress((char)8);                       
        delay(50);
        blehid.keyRelease();
        digitalWrite(BUZZER, LOW);      // v0.3f
      }
    }
    else 
    {
      keycheck = 1;
    }
  #endif
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

void handleConMouseMovement(void)    // v0.3
{
  if(flag_mouseConMovement == MOUSE_MOVE_RIGHT)
  {    
    blehid.mouseMove(mouseMoveStep, 0);
  }
  else if(flag_mouseConMovement == MOUSE_MOVE_LEFT)
  {
    blehid.mouseMove(-mouseMoveStep, 0);
  }
  else if(flag_mouseConMovement == MOUSE_MOVE_UP)
  {
    blehid.mouseMove(0, -mouseMoveStep);
  }
  else if(flag_mouseConMovement == MOUSE_MOVE_DOWN)
  {
    blehid.mouseMove(0, mouseMoveStep);
  }
  else if(flag_mouseConMovement == MOUSE_MOVE_LEFT_UP)        // v0.3e
  {
    blehid.mouseMove(-mouseMoveStep, -mouseMoveStep);
  }
  else if(flag_mouseConMovement == MOUSE_MOVE_RIGHT_UP)       // v0.3e
  {
    blehid.mouseMove(mouseMoveStep, -mouseMoveStep);
  }
  else if(flag_mouseConMovement == MOUSE_MOVE_LEFT_DOWN)      // v0.3e
  {
    blehid.mouseMove(-mouseMoveStep, mouseMoveStep);
  }
  else if(flag_mouseConMovement == MOUSE_MOVE_RIGHT_DOWN)     // v0.3e
  {
    blehid.mouseMove(mouseMoveStep, mouseMoveStep);
  }
}

void handleRepeatCmdAction(void)     // v0.3e
{
  if(lastSentCmdType == REG_KEYBOARD_CHAR)
  {
    blehid.keyPress((char)lastKeyboardChar);
    delay(20);        
    blehid.keyRelease(); 
  }
  else if(lastSentCmdType == SPL_KEYBOARD_CHAR)
  {
    keycodeComboBuff[0] = lastKeyboardChar;
    hidSpecialKeyPress((uint8_t*)keycodeComboBuff); 
  }
  else if(lastSentCmdType == MOUSE_CMD)
  {
    handleConMouseMovement();
  }
}
