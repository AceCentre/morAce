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

#define NUMPIXELS 1       // v0.2

// Variable Declarations
BLEDis bledis;
BLEHidAdafruit blehid;
Adafruit_NeoPixel pixels(NUMPIXELS, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);    // v0.2

const int BUTTON_ONE = KEY_ONE;
const int BUTTON_TWO = KEY_TWO;
const int BUTTON_THREE = KEY_THREE;
const int USER_BUTTON = USER_SWITCH;
int BUZZER = BUZZER_PIN;
const char DOT = '.';
const char DASH = '-';

volatile unsigned long t1,t2;
volatile unsigned long currentMillis;
const uint16_t charLength = (DOT_LENGTH * 3) + 100;
const char deviceBleName[] = DEVICE_BLE_NAME;
const char deviceManuf[] = DEVICE_MANUFACTURER;
const char deviceModelName[] = DEVICE_MODEL_NAME;
volatile char codeStr[MORSE_CODE_MAX_LENGTH];
volatile uint8_t codeStrIndex;
volatile char tempChar;
volatile uint32_t signal_len;
volatile uint8_t keyscan;
volatile uint16_t connectionHandle;
BLEConnection* connection = NULL;
volatile char central_name[32] = {0};
volatile char lastCentral_name[32] = {0};
volatile uint8_t flag_manualDisconnection;
volatile unsigned long manualDisconnTicks;
volatile uint8_t hidMode = KEYBOARD_MODE;

// Functions Declarations
void startBleAdvertising(void);
void checkButton(uint8_t buttonNum);
void checkButtonThreeForEndChar(void);
void bleConnectCallback(uint16_t conn_handle);
void setNeopixelColor(uint8_t r, uint8_t g, uint8_t b);   // v0.2

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
  pinMode(BUZZER,OUTPUT);
  digitalWrite(BUZZER, HIGH);

  pixels.begin();         // v0.2

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
  startBleAdvertising();

  // Set Neopixel Colour
  setNeopixelColor(0, 150, 0);    // v0.2   - Green Colour
}

void loop()
{
  currentMillis = millis(); 

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

  if(flag_manualDisconnection)
  {
    if(currentMillis - manualDisconnTicks >= LAST_CONNECTION_CHECK_TIMEOUT)
    {
      memset((char*)lastCentral_name, '\0', sizeof(lastCentral_name));
      flag_manualDisconnection = 0;     
    }
  }    

  checkForConnectionSwap();
  
}


void checkButton(uint8_t buttonNum)
{
  JUMP:
  if(digitalRead(buttonNum) == LOW)
  {    
    t1 = millis();                            //time at button press
    digitalWrite(BUZZER, LOW);               //LED on while button pressed
    while(digitalRead(buttonNum) == LOW && millis() - t1 < 2000);
    t2 = millis();                            //time at button release
    digitalWrite(BUZZER, HIGH);                //LED off on button release  
    
    signal_len = t2 - t1;                     //time for which button is pressed
    if(signal_len > 50)                      //to account for switch debouncing
    {
      #ifdef ONE_BUTTON_MODE
        codeStr[codeStrIndex++] += findDotOrDash();               //function to read dot or dash 
      #endif
      
      #ifdef TWO_BUTTON_MODE
        if(buttonNum == BUTTON_ONE)
        {
          //tempChar = findDot();
          tempChar = DOT;         // v0.2
          if(tempChar != NULL)
          {
            codeStr[codeStrIndex++] += tempChar;
          }          
        }
        else if(buttonNum == BUTTON_TWO)
        {
          //tempChar = findDash();
          tempChar = DASH;        // v0.2
          if(tempChar != NULL)
          {
            codeStr[codeStrIndex++] += tempChar;
          } 
        }
      #endif

      #ifdef THREE_BUTTON_MODE
        if(buttonNum == BUTTON_ONE)
        {
          //tempChar = findDot();
          tempChar = DOT;         // v0.2
          if(tempChar != NULL)
          {
            codeStr[codeStrIndex++] += tempChar;
          }          
        }
        else if(buttonNum == BUTTON_TWO)
        {
          //tempChar = findDash();
          tempChar = DASH;        // v0.2
          if(tempChar != NULL)
          {
            codeStr[codeStrIndex++] += tempChar;
          } 
        }
      #endif          
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

  #ifdef TWO_BUTTON_MODE
    if((millis() - t2) >= charLength || codeStrIndex >= MORSE_CODE_MAX_LENGTH)
    {
      if(codeStrIndex >= 1)
      {
        convertor();
        codeStrIndex = 0;
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
    convertor();
    codeStrIndex = 0;
  }
  else{}  
}

void checkForConnectionSwap(void)
{
  if((currentMillis % 100) == 0)
  {
    if(digitalRead(USER_BUTTON) == LOW)
    {
      if(keyscan)
      {
        keyscan = 0;
        #if SERIAL_DEBUG_EN
        Serial.println("Connection Swap Switch Pressed");
        #endif

        connectionHandle = Bluefruit.connHandle();
        
        connection = Bluefruit.Connection(connectionHandle);
        if(connection->connected())
        {
          if(connection->disconnect())
          {
            #if SERIAL_DEBUG_EN
            Serial.println("Disconnected");
            #endif
            flag_manualDisconnection = 1;
            manualDisconnTicks = millis();
          }
          else
          {
            #if SERIAL_DEBUG_EN
            Serial.println("Disconnection ERROR");
            #endif
          }
        }
        else
        {
          #if SERIAL_DEBUG_EN
          Serial.println("Not Connected");
          #endif
        }        
      }      
    }
    else
    {
      keyscan = 1;
    }
  }
}

void startBleAdvertising(void)
{  
  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();
  Bluefruit.Advertising.addAppearance(BLE_APPEARANCE_HID_KEYBOARD);
  Bluefruit.Advertising.addAppearance(BLE_APPEARANCE_HID_MOUSE);
  Bluefruit.Advertising.addService(blehid);
  Bluefruit.Advertising.addName();  
  Bluefruit.Advertising.restartOnDisconnect(true);
  Bluefruit.Advertising.setInterval(32, 244);
  Bluefruit.Advertising.setFastTimeout(30);
  Bluefruit.Advertising.start(0);
}

void bleConnectCallback(uint16_t conn_handle)
{
  connection = Bluefruit.Connection(conn_handle);  
  
  connection->getPeerName((char*)central_name, sizeof(central_name));  

  #if SERIAL_DEBUG_EN
  Serial.print("Connected to ");
  Serial.println((char*)central_name);
  #endif

  if(flag_manualDisconnection && !strcmp((char*)central_name, (char*)lastCentral_name))
  {
    #if SERIAL_DEBUG_EN
    Serial.print("Last Connection is same, Disconnecting...");
    #endif
    if(connection->disconnect())
    {
      #if SERIAL_DEBUG_EN
      Serial.println("Done");
      #endif
    }
    else
    {
      #if SERIAL_DEBUG_EN
      Serial.println("ERROR");
      #endif
    }
  }
  else
  {
    #if SERIAL_DEBUG_EN
    Serial.println("New Connection");
    #endif
    strcpy((char*)lastCentral_name, (char*)central_name);
    flag_manualDisconnection = 0;
  }
}

void setNeopixelColor(uint8_t r, uint8_t g, uint8_t b)    // v0.2
{
  pixels.clear();
  pixels.setPixelColor(0, pixels.Color(r, g, b));
  pixels.show();
}
