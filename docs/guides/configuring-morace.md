# Configuring morAce

{% hint style="info" %}
You dont have to use our circuitPy code using the Ace Centre's **x80 board**. Its a board that allows simpler way of accessing switches and adds a buzzer to a Adafruit board. But if you do its certainly a lot easier as no soldering required.&#x20;
{% endhint %}

You have some options depending on your needs. You will find all settings in the `userConfig.py`. Note that text macros and the morse code key set is in `morseCode.py`.\
\
**One, Two or Three switch morse functionality**

By default the board is set to **one switch mode.** By using one switch the user needs to send a dot and dash character by holding down the switch at the correct timings. So if you do use this one switch mode be particularly careful of adjusting the Length of a dot setting which is default set to 200 ms (a dash by convention is three times the length of a dot).

In **two switch mode** - you need a switch to send the dot and another for the dash. You still need some timing skills to allow the system to distinguish the end of character time. If a user has difficulty with this you may want to use **3 switch mode.** In this mode the third switch is the end of character signal. e.g. \
****\
****In one switch mode. To send the letter "a" (dot dash) you would press the button for **200 ms**, release then press immediatley again for **600 ms.** You then need to leave for a short period of time before starting another letter.&#x20;

In two switch mode you would press switch one for any length of time, release and then press the second switch. Then wait the period of time before starting the next letter.&#x20;

In three switch mode you would press switch 1, then 2, then 3.\
****

**To configure** this - edit `userConfig.py` - by editing the following lines. Put a 1 against the option you want. Put a zero against the options you dont want.&#x20;

```
one_button_mode = 1
two_button_mode = 0
three_button_mode = 0
```

**Length of a dot**&#x20;

For one switch mode you should be aware its set at 200ms by default. You can make this longer or shorter by editing this setting

`dot_length = 200`

**Fast Typing**

Some users want to hold down there dot or dash characters. This makes text entry far faster but it can be hard to use if you are new to morse. To turn it on&#x20;

`fast_typing_mode = 0`

There are a plethora of other configuration settings in userConfig.py - which you are welcome to edit. Just [note the details](switch-control-mode-and-morse-mode.md) about saving to the board particularly if you want to use the switch control mode or access more than one Bluetooth device. You will need to press switch 1 & 3 to reset the saving function.

{% hint style="info" %}
We recommend reading the rest of this guide before editing them so you understand what they do.&#x20;
{% endhint %}

