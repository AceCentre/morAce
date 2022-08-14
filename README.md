# What is MorAce?

## morAce

morAce is a Arduino project designed to work with the [Adafruit nrf52840](https://www.adafruit.com/product/4062) range of arduino boards - and converts 1, 2 or 3 switch inputs into HID keyboard/Mouse commands. A mode switch allows the device to switch between connected devices meaning you can use this on different computers - with no software or cables since its over Bluetooth.

<p align="center">
  <a href="https://www.openaac.org"><img src="https://img.shields.io/badge/OpenAAC-%F0%9F%92%AC-red?style=flat\&link=https://www.openaac.org"></a>
  <img alt="GitHub" src="https://img.shields.io/github/license/acecentre/morace">
  <img alt="GitHub issues" src="https://img.shields.io/github/issues-raw/acecentre/morace">
  <img alt="Lines of code" src="https://img.shields.io/tokei/lines/github/acecentre/morace">
</p>

### What does it do exactly?

You can use switches (1, 2, or 3) to send morse code signals which are then intepreted by the morAce as Keyboard strokes or mouse movements. Its configurable by editing the arduino file. It will work on any device that listens to a Bluetooth keyboard our mouse - such as an iOS device, Mac, Windows devices. Also with a fourth switch you can change which device it is currently connected to. It cycles between already paired devices.

### Want all the docs

**Read it all here: https://docs.acecentre.org.uk/products/v/morace/**


### Why? Why not a different project?

We needed a BLE HID Switch->Morse system - that allowed swapping between several different devices - AND - switching between switch scanning and morse input.

### Credits

* Tania Finlayson - and her husband for developing (and general all round awesomeness) for building [TandemMaster](http://tandemmaster.org). Please buy one if you want to support this project
* Jim Lubin - and his fab Morse archive [here](https://www.makoa.org/jlubin/morsecode.htm)
* [Adaptive Design](https://www.adaptivedesign.org) - who have been great recently about pushing along the morse agenda
* Adafruit. For being amazing.
* [deeproadrash](https://www.freelancer.co.uk/u/deeproadrash) who helped immensely with a lot of the code on this project. TY!
* [f1andrew](https://github.com/f1andrew) -Andrii Pavlyshyn who has done a lot of the changes to circuitPy and ironed out a lot of bugs. 

### Similar projects

* [ATMakers - AirTalker](https://github.com/ATMakersOrg/AirTalker) - A really nice replica of the Adap2U sip/puff Morse code to keyboard/mouse system used by Jim Lubin. Its neat - runs on CircuitPython. The BLE libraries though arent full featured yet.
* [Morsel](https://github.com/derekyerger/morsel). One of the few that attempt to this project over bluetooth. Ours has a few more features than this.
* [Ketcha-K - morsekey project](https://github.com/ketcha-k/morsekey). This was a bit of a kickstart to do this project (see also [this thread on reddit](https://www.reddit.com/r/arduino/comments/gaplhs/usb\_morse\_key\_using\_pro\_micro/))
* [Milad Hajihassan, Makers Making Change - and the FAIO project](https://www.makersmakingchange.com/project/faio-feather-all-in-one-switch/) - a neat project which has some morse functionality built in using the [easymorse project](https://github.com/milador/EasyMorse). Also uses the feather. (See more at [FAIO Multiplexer](https://github.com/milador/FAIO\_Multiplexer))
* [OllieBck / MorseBLEKeyboard](https://github.com/OllieBck/MorseBLEKeyBoard) - a project to switch between switch scanning and using Gboard.
* [K3NG / Arduino CW Keyer](https://blog.radioartisan.com/arduino-cw-keyer/) - this project has EVERYTHING you would ever need for proper morse code. We doff our cap..

### License

[MIT](https://choosealicense.com/licenses/mit/)

