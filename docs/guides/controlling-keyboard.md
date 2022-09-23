# Controlling the keyboard

## The basics

In its default state morace is designed to work with one switch. But it can be used with 1,2 or 3 switches if you configure it that way. So in one switch mode you press for a length of time for a dot and a length of time for a dash and the gap of no sending any characters is what defines the ending of a encoded chunk (a letter or any morse encoded element). You can change these timings in the **userConstants.py** file if you so wish.\
\
There is also a **fast typing mode** - where holding down the switch will repeat a character. It best works with at least two switches. Using it with one switch requires _VERY_ good timing skills! By default this is off. You can turn it on by editing userConfig.py and setting the parameter of `fast_typing_mode` to 1

{% hint style="info" %}
By default morAce is set to go to keyboard mode first. But you can toggle between keyboard mode and mouse mode with **`.-.--`**&#x20;
{% endhint %}

### **Keyboard keys**

These are the pre-defined keys. You can customise these by editing [`user/morse_code.py`](../../morAce/user/morse\_code.py)``

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
* `-` t
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
* `-.----`?
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
* `.-.--.` Backspace
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

(There are also some special keys. For a full listing view them in [`user/morse_code.py`](../../morAce/user/morse\_code.py))

### Sending key combinations

In a typical keyboard you might need to send multiple keys being held down at once. To do this we need to use the **HOLD** and **RELEASE** codes

`.---.-. HOLD`

Send this command first to hold down any key/mouse click and then after send command for key/mouse clik you want to hold

when you are done holding down keys you can release using this command

`.---.-- RELEASE`

e.g. HOLD Ctrl C RELEASE will hold down the ctrl and C key - and then release it. (NB: You could use sticky keys too if you wish which is a built in feature to most operating systems).\
\
We do have another way for common combinations too:

### **Repeat Command**

An alternative way of holding a key is similar to what we do with mouse. You use this by typing a character, then pressing repeat - and it will repeat pressing that. Cancelling the repeat is with any press.

`.---.-`

### Macro Mode

If a user types `....----` in either mouse or keyboard mode then the standard key set (e.g. A-Z etc) can be used with a macro. A user can define these in `user/morse_code_shortcuts.py` This way you just remember which letter or number is the macro.&#x20;

```
morseCodeShortcutCmd = {
  ".-"     : "My favourite string here",
  "-..."   : "My password here",
  "---."   : [Keycode.LEFT_CONTROL, Keycode.C],
  "-.."    : "My Password string here",
  "."      : "First row\nSecond row",
```

Once the macro code is sent - it will revert back to the previous mouse or keyboard mode.&#x20;

So for example. \
\
In Keyboard mode:

`....----  (Macro Mode)`

`.- ("`My favourite string here`" is sent)`

`(Back to Keyboard mode)`

{% hint style="info" %}
Note you can use keycodes e.g. `[Keycode.LEFT_CONTROL, Keycode.C]` or strings with special characters e.g.`"First row\nSecond row"`. Just be aware of the language of the device you are typing into. You may need to set the keycode correctly for this to work reliably. See below for more information
{% endhint %}

{% hint style="info" %}
You might want to consider making use of the operating systems own keyboard shortcuts. For example this is available in MacOS and iOS. On iOS this is found under Settings->General-> Keyboards-> Text Replacement.
{% endhint %}

### Keymaps

Be aware that the way morAce works is its just a keyboard. It has no idea of language. What your recieving computers keyboard language is set to - it will send the key it thinks you are sending. You can either send real key presses e.g. `[Keycode.SHIFT, Keycode.FIVE]` will send the Shift key and the 5 key. On a computer which thinks it has a UK keyboard - that will emit a % but it maybe something else on a different language. Or you can send predefined key mappings - e.g. if you have "%" in either `user/morse_code.py` or _`user/morse_code_shortcuts.py the morAce code looks up the correct key mapping from`_`user/keymaps`  which defines this like&#x20;

```
"%" :  [Keycode.SHIFT, Keycode.FIVE],
```

You can define what a standard keymap it should be by setting the language in the top of morse_code.py and morse\_code\_shortcuts.py_&#x20;

```
# keymap that translates predefined string characters into keycodes
from user.keymaps.us_keymap import keyboard_keymap

```

You can find already defined **keymaps** in `user/keymaps`
