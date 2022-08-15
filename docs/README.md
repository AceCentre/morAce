# What is MorAce?

## morAce

morAce is a Arduino project designed to work with the [Adafruit nrf52840](https://www.adafruit.com/product/4062) range of arduino boards - and converts 1, 2 or 3 switch inputs into HID keyboard/Mouse commands. A mode switch allows the device to switch between connected devices meaning you can use this on different computers - with no software or cables since its over Bluetooth.

[![](https://camo.githubusercontent.com/34fbf282c2333bba3c13ec03404bed142c158529d54dde17177f6a254875b705/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4f70656e4141432d2546302539462539322541432d7265643f7374796c653d666c61745c266c696e6b3d68747470733a2f2f7777772e6f70656e6161632e6f7267)](https://www.openaac.org/) [![GitHub](https://camo.githubusercontent.com/f63354035b4e6b615bbbd68af68d09081169b5eeab22186f920f2ba235c672df/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f61636563656e7472652f6d6f72616365)](https://camo.githubusercontent.com/f63354035b4e6b615bbbd68af68d09081169b5eeab22186f920f2ba235c672df/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f61636563656e7472652f6d6f72616365) [![GitHub issues](https://camo.githubusercontent.com/372218edee6d0732925be0eab972b95945f616429ea63e4e9e5e2add4d3e67a7/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6973737565732d7261772f61636563656e7472652f6d6f72616365)](https://camo.githubusercontent.com/372218edee6d0732925be0eab972b95945f616429ea63e4e9e5e2add4d3e67a7/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6973737565732d7261772f61636563656e7472652f6d6f72616365)

### What does it do exactly?

You can use switches (1, 2, or 3) to send morse code signals which are then intepreted by the morAce as Keyboard strokes or mouse movements. Its configurable by editing the arduino file. It will work on any device that listens to a Bluetooth keyboard our mouse - such as an iOS device, Mac, Windows devices. Also with a fourth switch you can change which device it is currently connected to. It cycles between already paired devices.

### Want to learn morse?

Try our [Morse-Learn](https://github.com/AceCentre/morse-learn/) Project.

Or if you are on a PC and want a way of learning how to use the mouse with visual feedback back try [MorseWriter](https://github.com/AceCentre/MorseWriter).

### Why is it called morAce? How should I pronounce that?!

More-Ace. or Maurice. Whatever you prefer. Thanks to [Michael Ritson](https://acecentre.org.uk/about/staff/michael-ritson) for naming this. Little did he know when he came up with that [Will Wade](https://acecentre.org.uk/about/staff/will-wade), who initally wrote this comes from a family where morse code and radio operating was talked about a lot as his dad - Maurice James Wade (Jim) spent his early years as a radio operator for Cable ships sailing the world.&#x20;

![Cable ship in Sydney, Australia](.gitbook/assets/photoboat.jpg) ![Jim Wade in the radio operators room](.gitbook/assets/photo.jpg)
