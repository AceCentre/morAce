# Controlling the mouse



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
