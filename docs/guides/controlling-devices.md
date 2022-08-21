# Controlling devices connected

{% hint style="danger" %}
Warning: This wont work unless you've enabled your morAce to write the filesystem. See [here](configuring-morace.md#want-to-pair-to-more-than-one-bluetooth-device-or-use-switch-control-mode) for how to do this.&#x20;
{% endhint %}

The command to change devices is&#x20;

`-.-.--`&#x20;

When this is sent morAce will drop connection with the current connected device and try connecting to the next last paired device. Note - if it doesnt connect within a set time frame (`last_connection_check_timeout`). It wil return back to the previous connected device.&#x20;

You can pair a new device once you go into this mode. The max number of devices you could connect to is set by `maxSwapConn`

{% hint style="info" %}
If you need morAce to forget all your paired devices you just need to delete the database on the circuitpy drive
{% endhint %}

