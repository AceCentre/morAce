# Controlling the mouse



**Mouse mode**

Once a device is connected by default it can send characters. But if you want to control it as a mouse you can enter the mouse mode. This is done with the morse command of `.-.--` (configurable in `userConfig.py`) and then the device can send mouse commands

_NB: in iOS you need to make sure Settings -> Accessibility -> AssistiveTouch -> On._

Then to move the mouse use these commands

| <p><br>Left Up<br>.--.</p> |   <p>Up<br>-</p>  | <p>Right Up<br>...-</p>     |
| -------------------------- | :---------------: | --------------------------- |
| <p>Left<br>..</p>          |                   | <p>Right<br>...</p>         |
| <p>Left Down<br>...--</p>  | <p>Down<br>--</p> | <p>Right Down<br>...---</p> |

By default it will only move 5 pixels (default is changeable - see `default_mouse_move_step` in `userConfig.p)`. If you wish the mouse to start moving in one direction and stop when you next send any switch press try using the **REPEAT** mode

. `Repeat Mode`

You would send the mouse movement you wish to do - THEN send the repeat command. Eg. Down - Repeat ( `--  .)` - will repeat moving down and stop on the first press.&#x20;

You can increase or decrease the **speed of movement** using some different options:&#x20;

`.-..--` Increase speed

`.-..-.` Decrease speed

`.--.-.` Set Speed to 1

`.--.--` Set Speed to 5

**Mouse buttons are:**

* `.--` Right Click
* `.-` Left Click
* `..--` Double Right click
* `..-` Double Left click

**Click and hold**

`-.` Left click and hold (enter again to toggle off)

`-.` Right click and hold (enter again to toggle this off)

So to drag the mouse you could use this technique. Or you could use the **REPEAT MOUSE** command (`.`)

#### To drag the mouse

`-. (Click and hold)` \
`-       (Up)` \
`.      (Repeat moving up)` \
`.      (release moving when ready)` \
`-.      (Release Click and Hold)`

