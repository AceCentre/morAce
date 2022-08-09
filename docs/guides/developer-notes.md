# Developer notes

So here by default filesystem is writable for microcontroller and read-only for external computer.\
When user wants to update files then it's needed to reset nrf board and right after press and hold 1 and 3 buttons until hearing long beep sound. That will mean that filesystem now available for firmware upload.



Currently in [boot.py](http://boot.py/) switching filesystem for microcontroller is commented so first time user can upload all files and check if buttons are working.
