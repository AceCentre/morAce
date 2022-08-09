# What is MorAce?

## morAce

morAce is a Arduino project designed to work with the [Adafruit nrf52840](https://www.adafruit.com/product/4062) range of arduino boards - and converts 1, 2 or 3 switch inputs into HID keyboard/Mouse commands. A mode switch allows the device to switch between connected devices meaning you can use this on different computers - with no software or cables since its over Bluetooth.

![OpenAAC](https://img.shields.io/badge/OpenAAC-%F0%9F%92%AC-red?style=flat\&link=https://www.openaac.org)

### What does it do exactly?

You can use switches (1, 2, or 3) to send morse code signals which are then intepreted by the morAce as Keyboard strokes or mouse movements. Its configurable by editing the arduino file. It will work on any device that listens to a Bluetooth keyboard our mouse - such as an iOS device, Mac, Windows devices. Also with a fourth switch you can change which device it is currently connected to. It cycles between already paired devices.

### Bill of materials

* x1 [Adafruit nrf52840](https://www.adafruit.com/product/4062)
* x3 [3.5mm Socket](https://www.hobbytronics.co.uk/stereo-audio-jack-socket) (or any [momentary buttons](https://www.hobbytronics.co.uk/push-switch-12mm))
* x1 [Buzzer](https://www.hobbytronics.co.uk/piezo-transducer-5v)
* x1 [PNP](https://www.hobbytronics.co.uk/bc212l-pnp-transistor)
* x1 [10K resistor](https://www.hobbytronics.co.uk/resistor-10k-1-8w)

### Arduino wiring

* **Pin** 10 - Morse Key 1 **State**: Active Low (External switch)
* **Pin** 11 - Morse Key 2 **State**: Active Low (External switch)
* **Pin** 12 - Morse Key 3 **State**: Active Low (External switch)
* **Pin** 5 - Buzzer **State**: Active Low (External switch)
* **USER Switch** - Switch for Connection Swapping **State**: Active Low (On board - Feather User SW)
* **CONN LED(Blue)** - LED indication for BLE Connection status **State**:Active High ("On board - Feather CONN LED - Blinking : Advertising, Not connected, Steady ON : Connected, Not advertising")

See also this [Fritzing diagram](https://github.com/AceCentre/BLEMorseToText/blob/master/ConnectionDiagram.fzz) :

![](https://raw.githubusercontent.com/AceCentre/BLEMorseToText/master/ConnectionDiagram.png)

#### Usage

Wire it all up. Set your settings in `userConfig.h`. Pair your device with a compatible device (PC, Mac, Linux, iOS, Android) - and away you go.

**More to follow here**

There **will** be bugs. Please submit them to the [issue queue](https://github.com/AceCentre/BLEMorseToText/issues).

**Keyboard keys**

These are the pre-defined keys. You can customise these by editing `morseCode.cpp`

* `.-` a
* `-...` b
* `---.` c
* `-..` d
* `.` e
* `..-.` f
* `--.` g
* `....` h
* `..` i
* `.---` j
* `-.-` k
* `.-..` l
* `--` m
* `-.` n
* `---` o
* `.--.` p
* `--.-` q
* `.-.` r
* `...` s
* `-"` t
* `..-` u
* `...-` v
* `.--` w
* `-..-` x
* `-.--` y
* `--..` z
* `-----` 0
* `.----` 1
* `..---` 2
* `...--` 3
* `....-` 4
* `.....` 5
* `-....` 6
* `--...` 7
* `---..` 8
* `----.` 9
* `----..` \\
* `....--` /
* `.--...` \[
* `-..---` ]
* `--..--` <
* `..--..` >
* `---...` (
* `...---` )
* `--..-` {
* `--..-` }
* `.-----` .
* `-.....` comma
* `----.-` \_
* `....-.` |
* `-.----` ?
* `.-....` !
* `-....-` ;
* `.----.` :
* `.---.` -
* `..----` $
* `...-.-` %
* `...--.` "
* `---..-` @
* `..-...` \\
* `--.---` backtick
* `-...--` ^
* `---.--` \~
* `..---.` #
* `.---..` &
* `-...-` +
* `---.-` =
* `-..--` \*
* `..--` Space
* `.-.-` Enter
* `--"` Backspace
* `--....` ESC
* `--...-` Shift
* `-.-.` Ctrl
* `--.--` Alt
* `.-..-` Arrow Up
* `.--..` Arrow Down
* `.-.-..` Arrow Left
* `.-.-.` Arrow Right
* `.....-` Pg Up
* `...-..` Pg Dn
* `.......` Home
* `...-...` End
* `---...-` Numlock
* `--.-..` ScrollLock
* `-----.` Capslock
* `-.-..` Insert
* `-.--..` Delete
* `--.--.` PrtScn
* `---..-.` Tab
* `--.----` F1
* `--..---` F2
* `--...--` F3
* `--....-` F4
* `--.....` F5
* `---....` F6
* `----...` F7
* `-----..` F8
* `------.` F9
* `-------` F10
* `.------` F11
* `..-----` F12

**Mouse mode**

Once a device is connected by default it can send characters. But if you want to control it as a mouse you can enter the mouse mode. This is done with the morse command of `.-.--` (configurable in userConfig.h) and then the device can send mouse commands

_NB: in iOS you need to make sure Settings -> Accessibility -> AssistiveTouch -> On._

Then to move the mouse it works in a way of automatic movement until you stop.

|                   |   <p>Up<br>-</p>  |                     |
| ----------------- | :---------------: | ------------------- |
| <p>Left<br>..</p> |                   | <p>Right<br>...</p> |
|                   | <p>Down<br>--</p> |                     |

Mouse buttons are:

* `.--` Right Click
* `.-` Left Click
* `..--` Double Right click
* `..-` Double Left click

**Change number of allowed connected devices**

By default the system is set for two devices. If morace is told to switch connected devices and the device isn't available after 5 seconds it reverts to the previously connected device.

If you want more devices simply change "MAXIMUM\_SWAP\_CONNECTIONS" in userConfig.h

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Files

All the Arduino code is in the sub-directory **Morse\_BLE\_HID**

* Morse\_BLE\_HID.ino - Main source code file
* morseCode.cpp - Library source code file for Morse Code related functions
* morseCode.h - Library header file for Morse Code related functions
* userConfig.h - Configuaration File for settings
* userPinMap.h - Pin mapping file

### Want to learn morse?

Try our [Morse-Learn](https://github.com/AceCentre/morse-learn/) Project.

Or if you are on a PC and want a way of learning how to use the mouse with visual feedback back try [MorseWriter](https://github.com/AceCentre/MorseWriter).

### Why? Why not a different project?

We needed a BLE HID Switch->Morse system - that allowed swapping between several different devices - AND - switching between switch scanning and morse input.

### Credits

* Tania Finlayson - and her husband for developing (and general all round awesomeness) for building [TandemMaster](http://tandemmaster.org). Please buy one if you want to support this project
* Jim Lubin - and his fab Morse archive [here](https://www.makoa.org/jlubin/morsecode.htm)
* [Adaptive Design](https://www.adaptivedesign.org) - who have been great recently about pushing along the morse agenda
* Adafruit. For being amazing.
* [deeproadrash](https://www.freelancer.co.uk/u/deeproadrash) who helped immensely with a lot of the code on this project. TY!

### Similar projects

* [ATMakers - AirTalker](https://github.com/ATMakersOrg/AirTalker) - A really nice replica of the Adap2U sip/puff Morse code to keyboard/mouse system used by Jim Lubin. Its neat - runs on CircuitPython. The BLE libraries though arent full featured yet.
* [Morsel](https://github.com/derekyerger/morsel). One of the few that attempt to this project over bluetooth. Ours has a few more features than this.
* [Ketcha-K - morsekey project](https://github.com/ketcha-k/morsekey). This was a bit of a kickstart to do this project (see also [this thread on reddit](https://www.reddit.com/r/arduino/comments/gaplhs/usb\_morse\_key\_using\_pro\_micro/))
* [Milad Hajihassan, Makers Making Change - and the FAIO project](https://www.makersmakingchange.com/project/faio-feather-all-in-one-switch/) - a neat project which has some morse functionality built in using the [easymorse project](https://github.com/milador/EasyMorse). Also uses the feather. (See more at [FAIO Multiplexer](https://github.com/milador/FAIO\_Multiplexer))
* [OllieBck / MorseBLEKeyboard](https://github.com/OllieBck/MorseBLEKeyBoard) - a project to switch between switch scanning and using Gboard.
* [K3NG / Arduino CW Keyer](https://blog.radioartisan.com/arduino-cw-keyer/) - this project has EVERYTHING you would ever need for proper morse code. We doff our cap..

### License

[MIT](https://choosealicense.com/licenses/mit/)

{% hint style="info" %}
**Good to know:** providing a brief overview of your product and its core use cases is a great place to start with product docs. Your product might seem obvious to you – you made it! However, to others, even folks who are trying your product after reading your site or getting a sales demo, it can still be unclear. This is your chance to clarify your product and set the right expectations!
{% endhint %}

Here are a couple of examples of succinct overviews from products with really great docs:

> Loom is a video messaging tool that helps you get your message across through instantly shareable videos.
>
> With Loom, you can record your camera, microphone, and desktop simultaneously. Your video is then instantly available to share through Loom's patented technology.
>
> — From the [Loom Docs](https://support.loom.com/hc/en-us/articles/360002158057-What-is-Loom-)

> The Mailchimp Marketing API provides programmatic access to Mailchimp data and functionality, allowing developers to build custom features to do things like sync email activity and campaign analytics with their database, manage audiences and campaigns, and more.
>
> — From the [Mailchimp Marketing API docs](https://mailchimp.com/developer/marketing/docs/fundamentals/)

## Getting Started

**Got 2 minutes?** Check out a video overview of our product:

{% embed url="https://www.loom.com/share/3bfa83acc9fd41b7b98b803ba9197d90" %}

{% hint style="info" %}
**Good to know:** A succinct video overview is a great way to introduce folks to your product. Embed a Loom, Vimeo or YouTube video and you're good to go! We love this video from the fine folks at [Loom](https://loom.com) as a perfect example of a succinct feature overview.
{% endhint %}

### Guides: Jump right in

Follow our handy guides to get started on the basics as quickly as possible:

{% content-ref url="guides/creating-your-first-project.md" %}
[creating-your-first-project.md](guides/creating-your-first-project.md)
{% endcontent-ref %}

{% content-ref url="guides/creating-your-first-task.md" %}
[creating-your-first-task.md](guides/creating-your-first-task.md)
{% endcontent-ref %}

{% content-ref url="guides/advanced-permissions.md" %}
[advanced-permissions.md](guides/advanced-permissions.md)
{% endcontent-ref %}

{% hint style="info" %}
**Good to know:** your product docs aren't just a reference of all your features! use them to encourage folks to perform certain actions and discover the value in your product.
{% endhint %}

### Fundamentals: Dive a little deeper

Learn the fundamentals of MyProduct to get a deeper understanding of our main features:

{% content-ref url="guides/projects.md" %}
[projects.md](guides/projects.md)
{% endcontent-ref %}

{% content-ref url="broken-reference" %}
[Broken link](broken-reference)
{% endcontent-ref %}

{% content-ref url="broken-reference" %}
[Broken link](broken-reference)
{% endcontent-ref %}

{% content-ref url="broken-reference" %}
[Broken link](broken-reference)
{% endcontent-ref %}

{% hint style="info" %}
**Good to know:** Splitting your product into fundamental concepts, objects, or areas can be a great way to let readers deep dive into the concepts that matter most to them. Combine guides with this approach to 'fundamentals' and you're well on your way to great documentation!
{% endhint %}
