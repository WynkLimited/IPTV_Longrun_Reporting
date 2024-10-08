from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage

import sys
import os
import time
import signal
import socket

"""
1.starts from Home 
2.Navigates through settings page 
3.performes satellite scan
4.Goes to live- 20min
5.Again launches home  
6.Clicks on Youtube 
7.Plays first content of youtube for - 20 min 
8.Launches Airtel Home
9.Navigates through setttings menu
10.jumps to LIVE content - plays LIVE for - 30min 
11. Starts channel Zpping in forward direction and zaps till 35 channel
"""

if len(sys.argv) > 1:
    device_ip = sys.argv[1]
    # device_ip = "192.168.1.63:5555"
else:
    print("please specify a device")
    sys.exit(1)


def create_folder_if_not_exists(foldername):
    folder_path = "./logs/" + foldername
    if not os.path.exists(folder_path):
        print("folder_path while creating folder " + folder_path)
        os.makedirs(folder_path)


def exitGracefully(self, signum, frame):
    signal.signal(signal.SIGINT, signal.getsignal(signal.SIGINT))
    device.shell('killall com.android.commands.monkey')
    sys.exit(1)


# append logs
def log(fn, device):
    msg = device.shell('logcat -d')
    f_log = open(fn, 'at')
    if msg is None:
        msg = 'None'
    f_log.write(msg.encode('utf-8'))
    f_log.close()
    device.shell('logcat -c')


# Connects to the current device, returning a MonkeyDevice object
print("waiting for connection...\n")
device = MonkeyRunner.waitForConnection(10, device_ip)
signal.signal(signal.SIGINT, exitGracefully)
device.shell('logcat -c')  # Clear logs buffer

package = 'com.airtel.tv'
activity = 'com.airtel.tv.MainActivity'

# sets the name of the component to start
runComponent = package + '/' + activity

# Runs the component
device.startActivity(component=runComponent)

print("launched activity")

create_folder_if_not_exists(device_ip[0:-5])
folder_path = os.getcwd()
current_file_path = os.path.abspath(__file__)
current_file_name = os.path.basename(current_file_path)

filename = folder_path + '/logs/' + device_ip[0:-5] + '/' + current_file_name[0:-3] + time.strftime(
    "%Y%m%d%H%M%S") + ".log"

while 1:
    try:
        # Variables
        menu_count = 9
        Repeatloop = 1

        # Launch Airtel home page
        device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
        print("Airtel Home button is pressed")
        log(filename, device)  # Write logs
        MonkeyRunner.sleep(2)

        # Back key pressed from opened Settings Page
        device.press("170", MonkeyDevice.DOWN_AND_UP)
        print("LIVE key is pressed")
        log(filename, device)  # Write logs
        MonkeyRunner.sleep(12)

        # Launch Airtel home page
        device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
        print("Airtel Home button is pressed")
        log(filename, device)  # Write logs
        MonkeyRunner.sleep(5)

        # Launch YouTube
        device.press("191", MonkeyDevice.DOWN_AND_UP)
        print("YouTube button is pressed")
        log(filename, device)  # Write logs
        MonkeyRunner.sleep(12)

        # Selecting first video from the YouTube Home Page
        device.press("DPAD_CENTER", MonkeyDevice.DOWN_AND_UP)
        print("Pressed on the first Video available in the YouTube Home Page")
        log(filename, device)  # Write logs
        MonkeyRunner.sleep(10)

        # Launch Airtel home page again
        device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
        print("Airtel Home button is pressed")
        log(filename, device)  # Write logs
        MonkeyRunner.sleep(2)

        # Navigating to Settings menu in Airtel home screen
        for i in range(1, menu_count):
            device.press("_RIGHT", MonkeyDevice.DOWN_AND_UP)
            print("Pressed RIGHT key %d time to navigate to Settings menu in Airtel home screen" % i)
            log(filename, device)  # Write logs
        MonkeyRunner.sleep(2)

        # Selecting Settings in Menu
        device.press("DPAD_CENTER", MonkeyDevice.DOWN_AND_UP)
        print("Selection key is pressed on Settings")
        log(filename, device)  # Write logs
        MonkeyRunner.sleep(5)

        # Navigating to LIVE
        device.press("170", MonkeyDevice.DOWN_AND_UP)
        print("LIVE Button is pressed")
        log(filename, device)  # Write logs
        MonkeyRunner.sleep(5)

        Chforward = 35
        # Channel change key forward movement
        for i in range(1, Chforward):
            device.press("CHANNEL_UP", MonkeyDevice.DOWN_AND_UP)
            print("Pressed channel up key for %d time" % i)
            MonkeyRunner.sleep(5)
            log(filename, device)  # Write logs
        MonkeyRunner.sleep(7)
    except socket.error:
        device.dispose()
