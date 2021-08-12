// Header Files
#include <bluefruit.h>
#include <BLEConnection.h>
#include <Adafruit_LittleFS.h>    // v0.3e
#include <InternalFileSystem.h>   // v0.3e
#include "userPinMap.h"
#include "userConfig.h"
#include "morseCode.h"

#if usesNeoPixel
	// Neopixel
	#include <Adafruit_NeoPixel.h>    // v0.2
#else
	// Dotstar
	#include <Adafruit_DotStar.h>
	#include <SPI.h>         // COMMENT OUT THIS LINE FOR GEMMA OR TRINKET
	//#include <avr/power.h> // ENABLE THIS LINE FOR GEMMA OR TRINKET
#endif

using namespace Adafruit_LittleFS_Namespace;        // v0.3e

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

// Type of Input                            // v0.3f
#define IP_NO_PULL      0
#define IP_PULLUP       1

// Type of Input pins for Morse keys        // v0.3f
#define MORSE_KEY_IP_TYPE       IP_NO_PULL  

// No of Neo-pixel LEDs or Dostar RGBs
#define NUMPIXELS      1       // v0.2

// Device Mode                 // v0.3c
#define MORSE_MODE      0
#define SW_CTRL_MODE    1

// Buzzer Pin                  // v0.3f
#if BUZZER_TYPE == ACTIVE_HIGH
  #define BUZZER_ON       digitalWrite(BUZZER, HIGH);
  #define BUZZER_OFF      digitalWrite(BUZZER, LOW);
#else
  #define BUZZER_ON       digitalWrite(BUZZER, LOW);
  #define BUZZER_OFF      digitalWrite(BUZZER, HIGH);
#endif

// Variable Declarations
BLEDis bledis;
BLEHidAdafruit blehid;
#if usesNeoPixel
	//Neopixel
	Adafruit_NeoPixel pixels(NUMPIXELS, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);    // v0.2
#else 
	Adafruit_DotStar strip(NUMPIXELS, DOTSTAR_DATA, DOTSTAR_CLOCK, DOTSTAR_BRG);
#endif 
SoftwareTimer softTimer;       // v0.3c
File dbFile(InternalFS);       // v0.3e

const int BUTTON_ONE = KEY_ONE;
const int BUTTON_TWO = KEY_TWO;
const int BUTTON_THREE = KEY_THREE;
const int USER_BUTTON = USER_SWITCH;
const int USER_BUTTON2 = USER_SWITCH2;
const int HARD_RESET_PIN = RESET_PIN;       // v0.3g
int BUZZER = BUZZER_PIN;
const char DOT = '.';
const char DASH = '-';

volatile unsigned long t1,t2;
volatile unsigned long currentMillis;
const char deviceBleName[] = DEVICE_BLE_NAME;
const char deviceBleName2[] = DEVICE_BLE_NAME2;     // v0.3c
const char deviceManuf[] = DEVICE_MANUFACTURER;
const char deviceModelName[] = DEVICE_MODEL_NAME;
const char boardTypeName[] = DEVICE_MODEL_NAME;
bool usesNeoPixel = USESNEOPIXEL;
volatile char codeStr[MORSE_CODE_MAX_LENGTH];
volatile uint8_t codeStrIndex;
volatile char tempChar;
volatile uint32_t signal_len;
volatile uint8_t keyscan;
volatile char lastCentral_name[32] = {0};
volatile uint8_t flag_manualDisconnection;
volatile unsigned long manualDisconnTicks;
volatile uint8_t hidMode = DEFAULT_MODE_OF_DEVICE;    // v0.3e
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
volatile uint8_t flag_repeatCmdEnable = 0;        // v0.3e
volatile unsigned long lastRepeatCmdSentTicks;    // v0.3e
volatile uint8_t mouseMoveStep = DEFAULT_MOUSE_MOVE_STEP; // v0.3e
const char dbFileName[] = "/database.txt";        // v0.3e

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
void readDataFromFS(void);                                // v0.3e
void writeDataToFS(void);                                 // v0.3e
void changeMacAddress(void);                              // v0.3g

// Functions Definations
void setup()
{
  // Begin Serial
  #if SERIAL_DEBUG_EN
  Serial.begin(115200);
  //while ( !Serial ) delay(10);                            // v0.3e // temp
  #endif

  // Configure GPIOs
  #ifdef ONE_BUTTON_MODE
    #if MORSE_KEY_IP_TYPE == IP_NO_PULL     // v0.3f     
      pinMode(BUTTON_ONE, INPUT);
    #else
      pinMode(BUTTON_ONE, INPUT_PULLUP);
    #endif
  #endif

  #ifdef TWO_BUTTON_MODE
    #if MORSE_KEY_IP_TYPE == IP_NO_PULL     // v0.3f    
      pinMode(BUTTON_ONE, INPUT);
      pinMode(BUTTON_TWO, INPUT);
    #else
      pinMode(BUTTON_ONE, INPUT_PULLUP);
      pinMode(BUTTON_TWO, INPUT_PULLUP);
    #endif
  #endif

  #ifdef THREE_BUTTON_MODE
    #if MORSE_KEY_IP_TYPE == IP_NO_PULL     // v0.3f    
      pinMode(BUTTON_ONE, INPUT);
      pinMode(BUTTON_TWO, INPUT);
      pinMode(BUTTON_THREE, INPUT);
    #else
      pinMode(BUTTON_ONE, INPUT_PULLUP);
      pinMode(BUTTON_TWO, INPUT_PULLUP);
      pinMode(BUTTON_THREE, INPUT_PULLUP);
    #endif
  #endif
  
  pinMode(USER_BUTTON, INPUT_PULLUP);
  pinMode(USER_BUTTON2, INPUT_PULLUP);           // v0.3b
  pinMode(BUZZER,OUTPUT);
  BUZZER_OFF;                                    // v0.3f

  pinMode(HARD_RESET_PIN, OUTPUT);               // v0.3g
  digitalWrite(HARD_RESET_PIN, HIGH);
  
  // Initialize Neopixel or dotstar
  #if usesNeoPixel
  		pixels.begin();                                // v0.2
	  	// Set Neopixel Colour
		setNeopixelColor(0, 0, 0);    // Off           // v0.3c
  #else
	  // Dotstar
	  strip.begin();
	  strip.show(); // Initialize all pixels to 'off'
  #endif 
  
  // Initialize Timer for 500 ms and start it
  softTimer.begin(500, softTimer_callback);      // v0.3c
  softTimer.start();                             // v0.3c

  // Initialize Internal File System
  InternalFS.begin();                            // v0.3e

  // Read Data from Internal File
  readDataFromFS();                              // v0.3e

  // Configure Bluefruit Parameters  
  Bluefruit.begin();  
  Bluefruit.setTxPower(4);

  if(currMode == MORSE_MODE)                     // v0.3g
  {
    Bluefruit.setName(deviceBleName);
  }
  else
  {
    Bluefruit.setName(deviceBleName2);
  }
  
  Bluefruit.Periph.setConnectCallback(bleConnectCallback);
  bledis.setManufacturer(deviceManuf);
  bledis.setModel(deviceModelName);

  // Set Device MAC Address
  changeMacAddress();                           // v0.3g

  // Begin BLE Services
  bledis.begin();
  
  // Begin BLE-HID Service
  blehid.begin(); 

  // Start BLE Advertising
  startBleAdvertising();                 // v0.3c
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

      // Write updated data into FS
      writeDataToFS();                              // v0.3e
    }
  }

  /*if(flag_mouseConMovement)               // v0.3
  {
    if(currentMillis - lastMouseMovTicks >= INTERVAL_SEND_MOUSE_MOVE_CMD)
    {
      lastMouseMovTicks = currentMillis;
      handleConMouseMovement();
    }    
  }*/   // Commented in v0.3e

  if(flag_repeatCmdEnable)                // v0.3e
  {
    if(currentMillis - lastRepeatCmdSentTicks >= INTERVAL_SEND_REPEAT_CMD)
    {
      lastRepeatCmdSentTicks = currentMillis;
      handleRepeatCmdAction();     
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
          BUZZER_ON;                            // v0.3f
          if(buttonNum == BUTTON_ONE)
          {
            codeStr[codeStrIndex++] += DOT;
          }
          else
          {
            codeStr[codeStrIndex++] += DASH;
          }
          delay(50);           
          BUZZER_OFF;                            // v0.3f
        }        
      }     
    }      
    else
    {
      t1 = millis();
      BUZZER_ON;                                 // v0.3f
      while(digitalRead(buttonNum) == LOW && millis() - t1 < 2000);
      t2 = millis();
      BUZZER_OFF;                                // v0.3f
    
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
    BUZZER_ON;                            // v0.3f
    convertor();
    codeStrIndex = 0;
    BUZZER_OFF;                           // v0.3f
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
        //uint16_t connectionHandle = 0;
        //BLEConnection* connection = NULL;
        
        keyscan = 0;
/*
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
*/
        // v0.3g
        // Hard Reset
        
        // Before reseting MCU, Do not disconnect BLE
        // Change Switch control/Morse mode variables
        // Write into FS

        // Then Reset MCU
        
        // After Reset
        // Read FS - Update variables
        // Take MAC & BLE advt. name accordingly
        // Start Advt.
        
        
        // v0.3g
        
        if(!flag_switchControlMode)
        {
          flag_switchControlMode = 1;
          currMode = SW_CTRL_MODE;              // v0.3e  
          #if SERIAL_DEBUG_EN
          Serial.println("Switch Control Mode Enable");
          #endif
        }
        else
        {
          flag_switchControlMode = 0;
          currMode = MORSE_MODE;               // v0.3e
          #if SERIAL_DEBUG_EN
          Serial.println("Switch Control Mode Disable");
          #endif
        }

        // Write updated data into FS
        writeDataToFS();                        // v0.3e

        // v0.3g
        #if SERIAL_DEBUG_EN
        Serial.println("Reseting MCU");
        delay(2000);
        #endif
        digitalWrite(HARD_RESET_PIN, LOW);
        // v0.3g
      }
    }
    else      // v0.3b
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
  Bluefruit.ScanResponse.addName();                 // v0.3c
  Bluefruit.Advertising.start();
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
        
        strip.setPixelColor(0, 0, 0, 0); //Off
        
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

    // Write updated data into FS
    writeDataToFS();                              // v0.3e
       
    flag_manualDisconnection = 0;
  }  
}

void setNeopixelColor(uint8_t r, uint8_t g, uint8_t b)    // v0.2
{
  #if usesNeoPixel
  //Neopoxel
	pixels.clear();
  	pixels.setPixelColor(0, pixels.Color(r, g, b));
  	pixels.show();
  #else
  //Dotstar
  	strip.clear();
  	strip.setPixelColor(0, r, g, b);
  	strip.show();
  #endif
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

void readDataFromFS(void)                                // v0.3e
{
  /*// temp
  currMode = 0;
  hidMode = 1;
  mouseMoveStep = 5;
  strcpy(swapConnDeviceNames[0], "");
  strcpy(swapConnDeviceNames[1], "");
  strcpy(swapConnDeviceNames[2], "");
  strcpy(swapConnDeviceNames[3], "");
  strcpy(swapConnDeviceNames[4], "");
  currSwapConnIndex = 0;
  writeDataToFS();
  // temp*/
  
  dbFile.open(dbFileName, FILE_O_READ);
  if(dbFile)
  {
    //#if SERIAL_DEBUG_EN
    //Serial.println("DB file open");
    //#endif

    uint32_t readlen;
    char buff[182] = { 0 };
    uint8_t str_valid = 0;
    
    readlen = dbFile.read(buff, sizeof(buff));

    buff[readlen] = 0;
    /*#if SERIAL_DEBUG_EN
    Serial.println(buff);
    #endif*/

    if(buff[0] == '@')
    {
      uint8_t comma_cnt = 0;
      for(uint8_t i = 0; i < sizeof(buff); i++)
      {
        if(buff[i] == ',')
        {
          comma_cnt++;
        }
        else if(buff[i] == '#')
        {
          if(comma_cnt == 8)
          {
            str_valid = 1;
          }
          break;
        }
      }
    }

    if(str_valid)
    {
      //#if SERIAL_DEBUG_EN
      //Serial.println("String is valid");
      //#endif

      uint16_t tmp_char = 0;
      uint8_t comma_cnt = 0;
      char str[32] = {0};
      uint8_t cnt = 0;
      
      tmp_char = atoi(&buff[1]);
      if(tmp_char == 0 || tmp_char == 1)
      {
        currMode = tmp_char;
      }
      else
      {
        currMode = MORSE_MODE;
      }

      // v0.3g
      if(currMode == MORSE_MODE)
      {
        flag_switchControlMode = 0;
      }
      else
      {
        flag_switchControlMode = 1;
      }
      // v0.3g

      for(uint8_t i = 0; i < sizeof(buff); i++)
      {
        if(buff[i] == ',')
        {
          comma_cnt++;
          if(comma_cnt == 2)
          {
            tmp_char = atoi(str);
            if(tmp_char == 0 || tmp_char == 1)
            {
              hidMode = (uint8_t)tmp_char;
            }
            else
            {
              hidMode = DEFAULT_MODE_OF_DEVICE;
            }
          }
          else if(comma_cnt == 3)
          {
            tmp_char = atoi(str);
            if(tmp_char > MOUSE_SPEED_LOWER_LIMIT && tmp_char <= MOUSE_SPEED_UPPER_LIMIT)
            {
               mouseMoveStep = tmp_char;
            }
            else
            {
              mouseMoveStep = DEFAULT_MOUSE_MOVE_STEP;
            }
          }
          else if(comma_cnt == 4)
          {
            strcpy(swapConnDeviceNames[0], str);
          }
          else if(comma_cnt == 5)
          {
            strcpy(swapConnDeviceNames[1], str);
          }
          else if(comma_cnt == 6)
          {
            strcpy(swapConnDeviceNames[2], str);
          }
          else if(comma_cnt == 7)
          {
            strcpy(swapConnDeviceNames[3], str);
          } 
          else if(comma_cnt == 8)
          {
            strcpy(swapConnDeviceNames[4], str);
          }          

          memset(str, '\0', sizeof(str));
          cnt = 0;
        }
        else if(buff[i] == '#')
        { 
          tmp_char = atoi(str);
          if(tmp_char < MAXIMUM_SWAP_CONNECTIONS)
          {
             currSwapConnIndex = tmp_char;
          }
          else
          {
            currSwapConnIndex = 0;
          }
          
          #if SERIAL_DEBUG_EN
          Serial.println("-------------------------------------------");
          Serial.println("Dev Mode:" + String(currMode));
          Serial.println("Morse Mode:" + String(hidMode));
          Serial.println("Mouse Step:" + String(mouseMoveStep));
          Serial.println("Name1:" + String(swapConnDeviceNames[0]));
          Serial.println("Name2:" + String(swapConnDeviceNames[1]));
          Serial.println("Name3:" + String(swapConnDeviceNames[2]));
          Serial.println("Name4:" + String(swapConnDeviceNames[3]));
          Serial.println("Name5:" + String(swapConnDeviceNames[4]));
          Serial.println("Swap Index:" + String(currSwapConnIndex));
          Serial.println("-------------------------------------------");
          #endif
          break;
        }
        else
        {
          str[cnt++] = buff[i];
        }
      }
    }
    else
    {
      #if SERIAL_DEBUG_EN
      Serial.println("String is not valid");
      #endif
      writeDataToFS();
    }
    dbFile.close();
  }
  else
  {
    #if SERIAL_DEBUG_EN
    Serial.println("DB file not present");
    #endif
    writeDataToFS();    
  }
}
void writeDataToFS(void)                                 // v0.3e
{
  char buff[182] = { 0 };
  memset(buff, '\0', sizeof(buff));
  sprintf(buff, "@%u,%u,%u,%s,%s,%s,%s,%s,%u#",
  currMode, hidMode, mouseMoveStep, swapConnDeviceNames[0], swapConnDeviceNames[1], swapConnDeviceNames[2], swapConnDeviceNames[3], swapConnDeviceNames[4], currSwapConnIndex);

  if(dbFile.open(dbFileName, FILE_O_WRITE))
  {
    dbFile.seek(0);
    dbFile.write(buff, strlen(buff));
    dbFile.close();
    #if SERIAL_DEBUG_EN
    Serial.println("Data written in DB file");
    #endif
  }
  else
  {
    #if SERIAL_DEBUG_EN
    Serial.println("DB file Write error");
    #endif
  }
}

void changeMacAddress(void)                           // v0.3g
{
  uint8_t mac[6] = {0};
  ble_gap_addr_t gap_addr;

  Bluefruit.getAddr(mac);
  /*Serial.print("Address Type: ");
  Serial.println(addr_type);
  for(int i = 0; i < 6; i++)
  {
    Serial.print(mac[i], HEX);
    Serial.print(' ');
  }
  Serial.println();*/
  
  gap_addr.addr_type = BLE_GAP_ADDR_TYPE_RANDOM_STATIC;
  gap_addr.addr[0] = mac[0];
  gap_addr.addr[1] = mac[1];
  gap_addr.addr[2] = mac[2];
  gap_addr.addr[3] = mac[3];
  gap_addr.addr[4] = mac[4];
  if(currMode == SW_CTRL_MODE)
  {
    gap_addr.addr[5] = 0xDD;
  }  

  if(Bluefruit.setAddr(&gap_addr))
  {
    #if SERIAL_DEBUG_EN
    Serial.println("MAC change Done");
    #endif
  }
  else
  {
    #if SERIAL_DEBUG_EN
    Serial.println("MAC change Error");
    #endif
  }

  memset(mac, '\0', sizeof(mac));
  Bluefruit.getAddr(mac);
  #if SERIAL_DEBUG_EN
  Serial.println("New MAC: ");
  for(int i = 0; i < 6; i++)
  {
    Serial.print(mac[i], HEX);
    Serial.print(' ');
  }
  Serial.println();
  #endif
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

  // Write updated data into FS
  writeDataToFS();                              // v0.3e
   
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
