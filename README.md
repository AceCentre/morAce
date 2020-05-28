# BLEMorseToText

BLEMorseToText is a Arduino project designed to work with the [Adafruit nrf52840](https://www.adafruit.com/product/4062) range of arduino boards - and converts 1, 2 or 3 switch inputs into HID keyboard/Mouse commands. A mode switch allows the device to switch between connected devices meaning you can use this on different computers.

![OpenAAC](https://img.shields.io/badge/OpenAAC-%F0%9F%92%AC-red?style=flat&link=https://www.openaac.org)

## Arduino wiring

* **Pin** 10 - Morse Key 1 	**State**: Active Low (External switch)
* **Pin** 11 - Morse Key 2	**State**: Active Low (External switch)
* **Pin** 12 - Morse Key 3	**State**: Active Low (External switch)
* **Pin** 5 - Buzzer **State**: Active Low (External switch)
* **USER Switch** - Switch for Connection Swapping	**State**: Active Low (On board - Feather User SW)
* **CONN LED(Blue)** - LED indication for BLE Connection status **State**:Active High ("On board - Feather CONN LED - Blinking : Advertising, Not connected, Steady ON : Connected, Not advertising")

See also this Fritzing diagram 

<img src="https://raw.githubusercontent.com/AceCentre/BLEMorseToText/master/ConnectionDiagram.png" width="600">


### Usage

Wire it all up. Set your settings in ``userConfig.h``. Pair your device with a compatible device (PC, Mac, Linux, iOS, Android) - and away you go.

**More to follow here**

There **will** be bugs. Please submit them to the [issue queue](https://github.com/AceCentre/BLEMorseToText/issues). 


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## Files

All the Arduino code is in the sub-directory **Morse_BLE_HID**

* Morse_BLE_HID.ino - Main source code file
* morseCode.cpp - Library source code file for Morse Code related functions
* morseCode.h - Library header file for Morse Code related functions
* userConfig.h - Configuaration File for settings
* userPinMap.h - Pin mapping file


## Want to learn morse?

Try our [Morse-Learn](https://github.com/AceCentre/morse-learn/) Project. 

Or if you are on a PC and want a way of learning how to use the mouse with visual feedback back try [MorseWriter](https://github.com/AceCentre/MorseWriter).

## Why? Why not a different project?

We needed a BLE HID Switch->Morse system - that allowed swapping between several different devices - AND - switching between switch scanning and morse input. 

## Credits

* Tania Finlayson - and her husband for developing (and general all round awesomeness) for building [TandemMaster](http://tandemmaster.org). Please buy one if you want to support this project
* Jim Lubin - and his fab Morse archive [here](https://www.makoa.org/jlubin/morsecode.htm)
* [Adaptive Design](https://www.adaptivedesign.org) - who have been great recently about pushing along the morse agenda
* Adafruit. For being amazing.

## Similar projects

* [Ketcha-K - morsekey project](https://github.com/ketcha-k/morsekey). This was a bit of a kickstart to do this project (see also [this thread on reddit](https://www.reddit.com/r/arduino/comments/gaplhs/usb_morse_key_using_pro_micro/))
* [Milad Hajihassan, Makers Making Change - and the FAIO project](https://www.makersmakingchange.com/project/faio-feather-all-in-one-switch/) - a neat project which has some morse functionality built in using the easymorse project. Also uses the feather. 
* [OllieBck / MorseBLEKeyboard](https://github.com/OllieBck/MorseBLEKeyBoard) - a project to switch between switch scanning and using Gboard. 
* [K3NG / Arduino CW Keyer](https://blog.radioartisan.com/arduino-cw-keyer/) - this project has EVERYTHING you would ever need for proper morse code. We doff our cap.. 


## License
[MIT](https://choosealicense.com/licenses/mit/)