from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import sys
import os
import time
import signal
import commonActions

if len(sys.argv) > 1:
    device_ip = sys.argv[1]
else:
    print("please specify a device")
    sys.exit(1)


def exitGracefully(self, signum, frame):
    signal.signal(signal.SIGINT, signal.getsignal(signal.SIGINT))
    device.shell('killall com.android.commands.monkey')
    sys.exit(1)


# Variables
iteration = 15
menu_count = 8
time_to_wait = 60 * 60 * 10
timeout = time.time() + time_to_wait
RowsBetweenBanners = 20

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

commonActions.create_folder_if_not_exists(device_ip[0:-5])
folder_path = os.getcwd()
current_file_path = os.path.abspath(__file__)
current_file_name = os.path.basename(current_file_path)
# print ("folder_path " + folder_path +"\n"+ "file" + __file__ + "\n current_file_path " + current_file_path + "\n current_file_name" + current_file_name)

filename = folder_path + '/logs/' + device_ip[0:-5] + '/' + current_file_name[0:-3] + time.strftime(
    "%Y%m%d%H%M%S") + ".log"
# filename = current_file_name[0:-3]+time.strftime("%Y%m%d%H%M%S") + ".log"

while 1:
    # Launch Airtel home page
    commonActions.click_home(filename, device, 5)

    # Navigating to Settings menu in Airtel home screen
    commonActions.continue_press(filename, device, "DPAD_DOWN", 2)

    # Navigate to APPS by pressing right key from search in menu
    commonActions.continue_press(filename, device, "DPAD_RIGHT", 0)

    # Selecting Apps in Menu
    commonActions.press_key(filename, device, "DPAD_CENTER", 10, "Selection key is pressed on APPS")

    # Navigate down to first rail under Apps
    commonActions.continue_press(filename, device, "DPAD_DOWN", 2)

    # Navigate right to hotstar app
    commonActions.continue_press(filename, device, "DPAD_RIGHT", 3)

    # Selecting Hotstar app
    commonActions.press_key(filename, device, "DPAD_CENTER", 10, "Selection key is pressed on hotstar app")

    # Selecting Hotstar app
    commonActions.press_key(filename, device, "DPAD_CENTER", 7, "Selection key is pressed on hotstar app")

    # Selecting Hotstar app
    commonActions.press_key(filename, device, "DPAD_CENTER", 1800, "Selection key is pressed on hotstar app")

    # Back to home page of the app
    commonActions.continue_press(filename, device, "KEYCODE_BACK", 4)

    print("Successfully played hotter content for  30 minutes")
    # device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
    print("Airtel Home button is pressed")
    commonActions.log(filename, device)  # Write logs
    print("end of script Hotstar playback")
    print("============================================================================================")
