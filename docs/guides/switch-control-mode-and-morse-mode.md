# Switch control mode

Some users may need to control their device with a built in switch scanning option - as well as use morse to type. To do this we have a neat method to enable this where the same device pretends to be a second bluetooth device.

{% hint style="danger" %}
Warning: This wont work unless you've enabled your morAce to write the filesystem. See [here](configuring-morace.md#want-to-pair-to-more-than-one-bluetooth-device-or-use-switch-control-mode) for how to do this.&#x20;
{% endhint %}

To swap between Morse and Switch mode - **Press switch 3. This toggles between the two.**&#x20;

Once you have done this a new BLE device is available known as **SW\_HID**. You should be able to connect to it and then setup switch access. By default the following keys are sent (depending on the button number you are using):\
\
**Button one mode:**\
****Button 1 - Space

**Button two mode:**\
****Button 1 - Space\
Button 2 - Enter

**Button three mode:**\
****Button 1 - Space\
Button 2 - Enter\
Button 3 - Backspace
