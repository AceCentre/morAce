# Switch control mode and Morse mode

Some users may need to control their device with a built in switch scanning option - as well as use morse to type. To do this we have a neat method to enable this where the same device pretends to be a second bluetooth device.

However to use this feature requires some steps.&#x20;

Uncomment some lines in `boot.py` notably lines 42, 48,49,50. I.e. this:

```
if button_one.value == False and button_two.value == True and button_three.value == False:    
    print("Filesystem ready for update.")
    #storage.remount("/", True)            
    extern.buzzer_set_state(True)
    time.sleep(2)
    extern.buzzer_set_state(False)
else:        
    print("Filesystem is readonly.")
    #storage.remount("/", False)    
    #print("data from file")
    #extern.readDataFromFS()

```

becomes:

```
if button_one.value == False and button_two.value == True and button_three.value == False:    
    print("Filesystem ready for update.")
    storage.remount("/", True)            
    extern.buzzer_set_state(True)
    time.sleep(2)
    extern.buzzer_set_state(False)
else:        
    print("Filesystem is readonly.")
    storage.remount("/", False)    
    print("data from file")
    extern.readDataFromFS()

```

We simply remove the **# (hash) marks**

Once done the device can write to the board itself.&#x20;

{% hint style="danger" %}
Warning. When you do this it will no longer by default load on the desktop and the config files cannot be edited.&#x20;
{% endhint %}

Next, Press switch **1 and 3** at the same time whilst booting up. i.e. unplug it and plug it in again to a power source.

To swap between Morse and Switch mode - **Press switch 3. This toggles between the two.**&#x20;

Once you have done this a new BLE device is available known as SW\_HID. You should be able to connect to it and then setup switch access.&#x20;
