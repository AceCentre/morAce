# Configuring morAce

{% hint style="info" %}
You dont have to use our circuitPy code using the Ace Centre's **x80**  but its easier. x80 is addon board for adafruit itsybitsy sized boards that allows simpler way of accessing switches and adds a buzzer to a Adafruit board. If you need to configure your adafruit nrf52840 feather express or nrf52840 itsybitsy - [read this guide. ](developer-notes.md)
{% endhint %}

### Starting off

If you have a brand new itsybitsy/x80 you will need to [read this guide](https://learn.adafruit.com/adafruit-itsybitsy-nrf52840-express/circuitpython) to get it in a state to be used with circuitpython. Once thats ready - you should have a disk drive mounted on your computer called "_CIRCUITPY_". Download[ all the code](https://github.com/AceCentre/morAce/archive/refs/heads/main.zip), unzip it and and then drag and drop the contents of **morAce/** directory to circuitpy.&#x20;

It should look like this (without boot\_out.xt, database.txt -or the lib directory).&#x20;

![If you do not have a lib folder - make that](<../.gitbook/assets/Screenshot 2022-08-14 at 10.00.38.png>)

Next you need to add some libraries to "lib" directory. If you are a developer we recommend using [circup](https://pypi.org/project/circup/). Simply type within the local directory&#x20;

```
circup install -r requirements.txt
```

If you are not - you'll need to install them by:

* [Downloading the bundle for 7.x](https://circuitpython.org/libraries)&#x20;
* Unzip&#x20;
* Drag the following flles to the "lib" folder on the CIRCUITPY drive: **adafruit\_dotstar,** **adafruit\_hid**, **adafruit\_ble** &#x20;

Once completed it should reboot. We recommend using [mu Editor](https://codewith.mu) to edit any userConfig.py files as you need to. Just note that bluetooth switching or using switch control mode wont work until you change a key file. More on that [below](configuring-morace.md#want-to-pair-to-more-than-one-bluetooth-device-or-use-switch-control-mode).&#x20;

### Key UserConfig Options

You have some options depending on your needs. You will find all settings in the `userConfig.py`. Note that text macros and the morse code key set is in `morseCode.py`.

**One, Two or Three switch morse functionality**

By default the board is set to **one switch mode.** By using one switch the user needs to send a dot and dash character by holding down the switch at the correct timings. So if you do use this one switch mode be particularly careful of adjusting the length of a dot setting which is default set to 200 ms (a dash by convention is three times the length of a dot).

In **two switch mode** - you need a switch to send the dot and another for the dash. You still need some timing skills to allow the system to distinguish the end of character time (set as the same time as a dot - so you would need to not press for **200ms**). If a user has difficulty with this you may want to use **3 switch mode.** In this mode the third switch is the end of character signal. e.g. \
****\
****In one switch mode. To send the letter "a" (dot dash) you would press **switch 1** for **200 ms**, release then press **switch 1** immediatley again for **600 ms.** You then need to leave for **minimum of 200ms** before starting another letter.&#x20;

In two switch mode you would press **switch one** for any length of time, release and then press the **second switch**. Then wait a **minimum of 200ms** before starting the next letter.&#x20;

In three switch mode you would press switch **1**, then **2**, then **3.**

**To configure** this - edit `userConfig.py` - by editing the following lines. Put a 1 against the option you want. Put a zero against the options you dont want.&#x20;

```
one_button_mode = 1
two_button_mode = 0
three_button_mode = 0
```

#### **Length of a dot**&#x20;

For one switch mode you should be aware its set at 200ms by default. You can make this longer or shorter by editing this setting

`dot_length = 200`

#### **Fast Typing**

Some users want to hold down there dot or dash characters. This makes text entry far faster but it can be hard to use if you are new to morse. To turn it on&#x20;

`fast_typing_mode = 0`

There are a plethora of other configuration settings in userConfig.py - which you are welcome to edit. Just [note the details](switch-control-mode-and-morse-mode.md) about saving to the board particularly if you want to use the switch control mode or access more than one Bluetooth device. You will need to press switch 1 & 3 to reset the saving function.

{% hint style="info" %}
We recommend reading the rest of this guide before editing them so you understand what they do.&#x20;
{% endhint %}

#### Sound (Buzzer) volume

See `sound_voiume` setting. Set it to 0-10 depending on how loud you want the buzzer feedback

### Want to Pair to more than one Bluetooth device or use switch control mode?

By default  the code **WILL NOT WORK** to use these two features. You will need to set the **saving\_parameters** **= True** in the userConfig.py file to allow this. This is because these modes need to write to the file system by itself - so if you want this we have to disable the neat USB disk drive feature of circuitPy. But dont worry - we've made it easy to switch it back on with a switch press so you can get back to editing the configuration. \
\
Once this parameter is set to True then restarting the morAce board will by default put it into a read only mode. You cannot edit config files. To allow editing config files **PRESS AND HOLD SWITCH ONE on reboot.** If you have no way of pulling the power on your own you can use this morse command to reset the power:&#x20;

`..-..-..` (Reset the power/MCU - set in UserConfig.py)

It will now allow you to edit files on the CIRCUITPY usb drive. But be aware - that if it restarts again it will go back to not allowing you to save to that directory.&#x20;

