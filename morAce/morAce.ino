// Header Files
#include <bluefruit.h>
#include <BLEConnection.h>
#include <Adafruit_NeoPixel.h>    // v0.2
#include "userPinMap.h"
#include "userConfig.h"
#include "morseCode.h"

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

// No of Neo-pixel LEDs
#define NUMPIXELS      1       // v0.2

// Device Mode                 // v0.3c
#define MORSE_MODE      0
#define SW_CTRL_MODE    1

// Variable Declarations
BLEDis bledis;
BLEHidAdafruit blehid;
Adafruit_NeoPixel pixels(NUMPIXELS, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);    // v0.2
SoftwareTimer softTimer;       // v0.3c

const int BUTTON_ONE = KEY_ONE;
const int BUTTON_TWO = KEY_TWO;
const int BUTTON_THREE = KEY_THREE;
const int USER_BUTTON = USER_SWITCH;
const int USER_BUTTON2 = USER_SWITCH2;
int BUZZER = BUZZER_PIN;
const char DOT = '.';
const char DASH = '-';

volatile unsigned long t1,t2;
volatile unsigned long currentMillis;
const char deviceBleName[] = DEVICE_BLE_NAME;
const char deviceBleName2[] = DEVICE_BLE_NAME2;     // v0.3c
const char deviceManuf[] = DEVICE_MANUFACTURER;
const char deviceModelName[] = DEVICE_MODEL_NAME;
volatile char codeStr[MORSE_CODE_MAX_LENGTH];
volatile uint8_t codeStrIndex;
volatile char tempChar;
volatile uint32_t signal_len;
volatile uint8_t keyscan;
volatile char lastCentral_name[32] = {0};
volatile uint8_t flag_manualDisconnection;
volatile unsigned long manualDisconnTicks;
volatile uint8_t hidMode = KEYBOARD_MODE;
volatile uint8_t flag_mouseConMovement = 0;     // v0.3
volatile unsigned long lastMouseMovTicks;       // v0.3
volatile unsigned long lastBeepTicks;           // v0.3
volatile unsigned long lastUserBtnCheckTicks;   // v0.3
volatile unsigned long lastScKeyCheckTicks;     // v0.3
volatile uint8_t flag_switchControlMode;        // v0.3
volatile unsigned char currMode = MORSE_MODE;   // v0.3c
const unsigned char maxSwapConn = MAXIMUM_SWAP_CONNECTIONS;     // v0.3c
volatile unsigned char currSwapConnIndex = 0;   // v0.3c
char swapConnDeviceNames[MAXIMUM_SWAP_CONNECTIONS][32] = {0};    // v0.3c
volatile unsigned char flag_blinkNeopixel = 0;    // v0.3c
volatile unsigned char flag_blinkOnOff = 0;       // v0.3c

/*
// v0.3c
const uint8_t CUSTOM_UUID_MORSE[] =
{
    0xA0, 0xDB, 0xD3, 0x6A, 0x00, 0xA6, 0xF7, 0x8C,
    0xE7, 0x11, 0x8F, 0x71, 0x1A, 0xFF, 0x67, 0xDF
};
const uint8_t CUSTOM_UUID_SW[] =
{
    0xA1, 0xDB, 0xD3, 0x6A, 0x00, 0xA6, 0xF7, 0x8C,
    0xE7, 0x11, 0x8F, 0x71, 0x1A, 0xFF, 0x67, 0xDF
};
// v0.3c

//BLEUuid uuidMorse = BLEUuid(CUSTOM_UUID_MORSE);     // v0.3c
//BLEUuid uuidSw = BLEUuid(CUSTOM_UUID_SW);           // v0.3c
*/

#if defined(TWO_BUTTON_MODE) || defined(THREE_BUTTON_MODE)  // v0.3
const uint8_t flag_fastTypingMode = FAST_TYPING_MODE;   
#else
const uint8_t flag_fastTypingMode = 0;
#endif

#ifdef FAST_TYPING_MODE                                     // v0.3
const uint16_t charLength = (DOT_LENGTH * 3) + 250;
#else
const uint16_t charLength = (DOT_LENGTH * 3) + 100;       
#endif

// Functions Declarations
void startBleAdvertising(void);
void checkButton(uint8_t buttonNum);
void checkButtonThreeForEndChar(void);
void bleConnectCallback(uint16_t conn_handle);
void setNeopixelColor(uint8_t r, uint8_t g, uint8_t b);   // v0.2
void handleBleConnectionSwap(void);                       // v0.3
void setNeopixelIndication(unsigned char index);          // v0.3c

// Functions Definations
void setup()
{
  // Begin Serial
  #if SERIAL_DEBUG_EN
  Serial.begin(115200);
  #endif

  // Configure GPIOs
  #ifdef ONE_BUTTON_MODE
    pinMode(BUTTON_ONE, INPUT_PULLUP);
  #endif

  #ifdef TWO_BUTTON_MODE
    pinMode(BUTTON_ONE, INPUT_PULLUP);
    pinMode(BUTTON_TWO, INPUT_PULLUP);  
  #endif

  #ifdef THREE_BUTTON_MODE
    pinMode(BUTTON_ONE, INPUT_PULLUP);
    pinMode(BUTTON_TWO, INPUT_PULLUP);
    pinMode(BUTTON_THREE, INPUT_PULLUP);
  #endif
  
  pinMode(USER_BUTTON, INPUT_PULLUP);
  pinMode(USER_BUTTON2, INPUT_PULLUP);           // v0.3b
  pinMode(BUZZER,OUTPUT);
  digitalWrite(BUZZER, HIGH);

  // Initialize Neopixel
  pixels.begin();                                // v0.2

  // Set Neopixel Colour
  setNeopixelColor(0, 0, 0);    // Off           // v0.3c

  // Initialize Timer for 500 ms and start it
  softTimer.begin(500, softTimer_callback);      // v0.3c
  softTimer.start();                             // v0.3c

  // Configure Bluefruit Parameters
  Bluefruit.begin();
  Bluefruit.setTxPower(4);
  Bluefruit.setName(deviceBleName);
  Bluefruit.Periph.setConnectCallback(bleConnectCallback);
  bledis.setManufacturer(deviceManuf);
  bledis.setModel(deviceModelName);

  // Begin BLE Services
  bledis.begin();
  
  // Begin BLE-HID Service
  blehid.begin();

  // Start BLE Advertising
  startBleAdvertising(currMode);                 // v0.3c  
}

void loop()
{
  currentMillis = millis();

  if(flag_switchControlMode)              // v0.3
  {
    if(currentMillis - lastScKeyCheckTicks >= 100)
    {
      lastScKeyCheckTicks = currentMillis;
      handleSwitchControlKeypress();
    }      
  }
  else
  {
    #ifdef ONE_BUTTON_MODE
      checkButton(BUTTON_ONE);
    #endif
  
    #ifdef TWO_BUTTON_MODE
      checkButton(BUTTON_ONE);
      checkButton(BUTTON_TWO); 
    #endif
  
    #ifdef THREE_BUTTON_MODE
      checkButton(BUTTON_ONE);
      checkButton(BUTTON_TWO);
      checkButtonThreeForEndChar();
    #endif
  }  

  if(flag_manualDisconnection)
  {
    if(currentMillis - manualDisconnTicks >= LAST_CONNECTION_CHECK_TIMEOUT)
    {
      memset((char*)lastCentral_name, '\0', sizeof(lastCentral_name));
      flag_manualDisconnection = 0;
      currSwapConnIndex = 0;              // v0.3c   
    }
  }

  if(flag_mouseConMovement)               // v0.3
  {
    if(currentMillis - lastMouseMovTicks >= INTERVAL_SEND_MOUSE_MOVE_CMD)
    {
      lastMouseMovTicks = currentMillis;
      handleConMouseMovement();
    }    
  }

  checkForConnectionSwap();
  
}


void checkButton(uint8_t buttonNum)
{
  JUMP:
  if(digitalRead(buttonNum) == LOW)
  {
    if(flag_fastTypingMode)           // v0.3
    {
      t1 = millis();
      lastBeepTicks = t1;      
      while(digitalRead(buttonNum) == LOW)
      {
        if(millis() - lastBeepTicks >= DOT_LENGTH)
        {
          lastBeepTicks = millis();
          digitalWrite(BUZZER, LOW);
          if(buttonNum == BUTTON_ONE)
          {
            codeStr[codeStrIndex++] += DOT;
          }
          else
          {
            codeStr[codeStrIndex++] += DASH;
          }
          delay(50);           
          digitalWrite(BUZZER, HIGH);
        }        
      }     
    }      
    else
    {
      t1 = millis();
      digitalWrite(BUZZER, LOW);
      while(digitalRead(buttonNum) == LOW && millis() - t1 < 2000);
      t2 = millis();
      digitalWrite(BUZZER, HIGH);
    
      signal_len = t2 - t1;
      if(signal_len > 50)
      {
        #ifdef ONE_BUTTON_MODE
          codeStr[codeStrIndex++] += findDotOrDash();               //function to read dot or dash 
        #endif
        
        #if defined(TWO_BUTTON_MODE) || defined(THREE_BUTTON_MODE)
          if(buttonNum == BUTTON_ONE)
          { 
            codeStr[codeStrIndex++] += DOT;     // v0.2                    
          }
          else if(buttonNum == BUTTON_TWO)
          { 
            codeStr[codeStrIndex++] += DASH;    // v0.2           
          }
        #endif // -#if define(TWO_BUTTON_MODE) || define(THREE_BUTTON_MODE)     
      }
    }   
  }    

  #ifdef ONE_BUTTON_MODE
    while((millis() - t2) < charLength && codeStrIndex < MORSE_CODE_MAX_LENGTH)
    {     
      if(digitalRead(buttonNum) == LOW)
      {   
        goto JUMP;     
      }
    }
  #endif

  #if defined(TWO_BUTTON_MODE)        // v0.3
    if(!flag_fastTypingMode)
    {
      if((millis() - t2) >= charLength || codeStrIndex >= MORSE_CODE_MAX_LENGTH)
      {
        if(codeStrIndex >= 1)
        {
          convertor();
          codeStrIndex = 0;
        } 
      }
    }
    else
    {
      if((millis() - lastBeepTicks) >= charLength || codeStrIndex >= MORSE_CODE_MAX_LENGTH)
      {
        if(codeStrIndex >= 1)
        {
          convertor();
          codeStrIndex = 0;
        } 
      }
    }
  #endif

  #ifdef THREE_BUTTON_MODE
    
  #endif
  
  #ifdef ONE_BUTTON_MODE
    if(codeStrIndex >= 1)
    {
      convertor();
      codeStrIndex = 0;
    }
    else{}
  #endif

  #ifdef TWO_BUTTON_MODE
    
  #endif
  
}

void checkButtonThreeForEndChar(void)
{
  if(codeStrIndex >= 1 && digitalRead(BUTTON_THREE) == LOW)
  {
    digitalWrite(BUZZER, LOW);      // v0.3
    convertor();
    codeStrIndex = 0;
    digitalWrite(BUZZER, HIGH);     // 0.3
  }
  else{}  
}

void checkForConnectionSwap(void)
{ 
  if(currentMillis - lastUserBtnCheckTicks >= 100)
  {
    lastUserBtnCheckTicks = currentMillis;
    if(digitalRead(USER_BUTTON) == LOW)
    {
      if(keyscan)       // v0.3b
      {
        keyscan = 0;
        #if SERIAL_DEBUG_EN
        Serial.println("Connection Swap Switch Pressed");
        #endif       
        
        handleBleConnectionSwap();      // v0.3        
      }           
    }
    else if(digitalRead(USER_BUTTON2) == LOW)       // v0.3b
    {
      if(keyscan)       
      {
        uint16_t connectionHandle = 0;
        BLEConnection* connection = NULL;
        
        keyscan = 0;

        // v0.3c
        Bluefruit.Advertising.stop();
        Bluefruit.Advertising.clearData();
        Bluefruit.ScanResponse.clearData();
        connectionHandle = Bluefruit.connHandle();                
        connection = Bluefruit.Connection(connectionHandle);        
        delay(1000);
        connection->disconnect();
        delay(2000);
        // v0.3c
        
        if(!flag_switchControlMode)
        {
          flag_switchControlMode = 1;
          #if SERIAL_DEBUG_EN
          Serial.println("Switch Control Mode Enable");
          #endif
          Bluefruit.setName(deviceBleName2);    // v0.3c
          startBleAdvertising(SW_CTRL_MODE);    // v0.3c
        }
        else
        {
          flag_switchControlMode = 0;
          #if SERIAL_DEBUG_EN
          Serial.println("Switch Control Mode Disable");
          #endif
          Bluefruit.setName(deviceBleName);    // v0.3c
          startBleAdvertising(MORSE_MODE);     // v0.3c
        }
      }
    }
    else      // v0.3b
    {      
      keyscan = 1;
    }
  }
}

void startBleAdvertising(unsigned char mode)
{  
  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();
  /*if(mode == MORSE_MODE)                        // v0.3c
  {
    Bluefruit.Advertising.addUuid(uuidMorse);
  }
  else
  {
    Bluefruit.Advertising.addUuid(uuidSw);
  } */
  Bluefruit.Advertising.addAppearance(BLE_APPEARANCE_HID_KEYBOARD);
  Bluefruit.Advertising.addAppearance(BLE_APPEARANCE_HID_MOUSE);
  Bluefruit.Advertising.addService(blehid);
  Bluefruit.Advertising.addName();  
  Bluefruit.Advertising.restartOnDisconnect(true);
  Bluefruit.Advertising.setInterval(32, 244);
  Bluefruit.Advertising.setFastTimeout(30);
  Bluefruit.ScanResponse.addName();           // v0.3c
  Bluefruit.Advertising.start(0);
}

void bleConnectCallback(uint16_t conn_handle)       // v0.3c
{
  int i = 0;
  uint16_t connectionHandle = 0;
  BLEConnection* connection = NULL;
  char central_name[32] = {0};
  
  connection = Bluefruit.Connection(conn_handle);  
  connection->getPeerName(central_name, sizeof(central_name));  

  #if SERIAL_DEBUG_EN
  Serial.print("Connection Req from ");
  Serial.println((char*)central_name);
  /*for(i = 0; i < maxSwapConn; i++)
  {
    Serial.print(i);
    Serial.print(": ");
    Serial.print(String((char*)swapConnDeviceNames[i]));
    Serial.print(", ");
  }
  Serial.println();*/
  #endif

  if(flag_manualDisconnection)
  {    
    for(i = 0; i < maxSwapConn; i++)
    {
      if(!strcmp((char*)central_name, (char*)swapConnDeviceNames[i]))
      {
        /*#if SERIAL_DEBUG_EN        
        Serial.print("Name matched in last list, Disconnecting...");
        #endif*/
        
        setNeopixelColor(0, 0, 0);      // Off      // v0.3c
        
        if(connection->disconnect())
        {
          #if SERIAL_DEBUG_EN
          Serial.println("Done");
          Serial.println();
          #endif
        }
        else
        {
          #if SERIAL_DEBUG_EN
          Serial.println("ERROR");
          #endif
        }
        break;
      }
    }    
  }
  
  if(i == maxSwapConn || !flag_manualDisconnection)
  {
    #if SERIAL_DEBUG_EN
    Serial.print("New Connection: ");
    Serial.println((char*)central_name);
    Serial.println();
    #endif

    // v0.3c
    flag_blinkNeopixel = 0;
    setNeopixelIndication(currSwapConnIndex);
    memset((char*)lastCentral_name, NULL, sizeof((char*)lastCentral_name));
    memset((char*)swapConnDeviceNames[currSwapConnIndex], NULL, sizeof((char*)swapConnDeviceNames[currSwapConnIndex]));
    memset((char*)swapConnDeviceNames[currSwapConnIndex+1], NULL, sizeof((char*)swapConnDeviceNames[currSwapConnIndex+1]));
    strcpy(swapConnDeviceNames[currSwapConnIndex], (char*)central_name);      
    strcpy((char*)lastCentral_name, (char*)central_name);
    // v0.3c
       
    flag_manualDisconnection = 0;
  }  
}

void setNeopixelColor(uint8_t r, uint8_t g, uint8_t b)    // v0.2
{
  pixels.clear();
  pixels.setPixelColor(0, pixels.Color(r, g, b));
  pixels.show();
}

void setNeopixelIndication(unsigned char index)           // v0.3c
{
  if(index == 0)
  {
    setNeopixelColor(0, 0, 255);      // Blue    
  }
  else if(index == 1)
  {
    setNeopixelColor(0, 255, 255);    // Cyan
  }
  else if(index == 2)
  {
    setNeopixelColor(0, 255, 0);      // Green
  }
  else if(index == 3)
  {
    setNeopixelColor(255, 255, 0);    // Yellow
  }
  else if(index == 4)
  {
    setNeopixelColor(255, 128, 0);    // Orange
  }
}

void handleBleConnectionSwap(void)      // v0.3
{
  uint16_t connectionHandle = 0;
  BLEConnection* connection = NULL;
  
  connectionHandle = Bluefruit.connHandle();        
  connection = Bluefruit.Connection(connectionHandle);

  // v0.3c
  currSwapConnIndex++;
  if(currSwapConnIndex >= maxSwapConn)
  {
    currSwapConnIndex = 0;
  }
  memset(swapConnDeviceNames[currSwapConnIndex], NULL, maxSwapConn);
  // v0.3c
   
  delay(2000); 
  connection->disconnect();
  #if SERIAL_DEBUG_EN 
  Serial.println("Disconnected");
  #endif
  
  setNeopixelColor(0, 0, 0);      // Off      // v0.3c
  flag_blinkNeopixel = 1;                     // v0.3c 

  flag_manualDisconnection = 1;
  manualDisconnTicks = millis();  
}

void softTimer_callback(TimerHandle_t xTimerID)       // v0.3c
{
  (void) xTimerID;
  if(flag_blinkNeopixel)
  {
    if(flag_blinkOnOff)
    {
      flag_blinkOnOff = 0;
      setNeopixelColor(0, 0, 0);      // Off
    }
    else
    {
      flag_blinkOnOff = 1;
      setNeopixelIndication(currSwapConnIndex);
    }   
  }  
}
