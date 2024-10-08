from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage

import sys
import os
import time
import signal
import socket


def log(fn, device):
    msg = device.shell('logcat -d')
    f_log = open(fn, 'at')
    if msg is None:
        msg = 'None'
    f_log.write(msg.encode('utf-8'))
    f_log.close()
    device.shell('logcat -c')


def exitGracefully(device):
    signal.signal(signal.SIGINT, signal.getsignal(signal.SIGINT))
    device.shell('killall com.android.commands.monkey')
    sys.exit(1)


def create_folder_if_not_exists(folder_name):
    folder_path = "./logs/" + folder_name
    if not os.path.exists(folder_path):
        print("folder_path while creating folder " + folder_path)
        os.makedirs(folder_path)


def click_home(filename, device, timeout):
    try:
        device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
        print("==>Airtel Home button is pressed")
    except:
        print("******* KEYCODE_HOME not pressed: *******")

    log(filename, device)
    MonkeyRunner.sleep(timeout)


def press_key(filename, device, key, timeout, message):
    try:
        device.press(key, MonkeyDevice.DOWN_AND_UP)
        print("==>" + message)
    except:
        print("*************")

    log(filename, device)
    MonkeyRunner.sleep(timeout)


def continue_press(filename, device, key, count):
    for i in range(0, count):
        try:
            device.press(key, MonkeyDevice.DOWN_AND_UP)
            print("==>Pressed %s key %d time" % (key, (i + 1)))
        except:
            print("*************")

        log(filename, device)  # Write logs
        MonkeyRunner.sleep(1)


def navigateToApp(filename, device, count, message):
    click_home(filename, device, 5)
    continue_press(filename, device, "DPAD_DOWN", 2)
    continue_press(filename, device, "DPAD_RIGHT", count)
    press_key(filename, device, "DPAD_CENTER", 5, message)
