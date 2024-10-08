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
menu_count = 8
NoOfRows = 4

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

while 1:

    # Launch Airtel home page
    commonActions.click_home(filename, device, 5)

    # Navigating to Settings menu in Airtel home screen
    commonActions.continue_press(filename, device, "DPAD_RIGHT", menu_count)
    MonkeyRunner.sleep(2)

    # Selecting Settings in Menu
    commonActions.press_key(filename, device, "DPAD_CENTER", 5, "Selection key is pressed on Settings")

    # Navigate down to second rail under Settings
    # commonActions.continue_press(filename, device, "DPAD_DOWN", 1)
    # MonkeyRunner.sleep(2)

    # Navigate across all the cards under Settings screen
    for row in range(NoOfRows):
        CardCount = 0
        while CardCount < 3:

            if row != 0 and CardCount != 0 or row != 1 and CardCount != 0:
                print("ROW====%d cardCount====%d" % (row, CardCount))
                MonkeyRunner.sleep(2)
                commonActions.press_key(filename, device, "DPAD_CENTER", 2, "Selection key is pressed")
                commonActions.press_key(filename, device, "KEYCODE_BACK", 2, "Back key is pressed")

            commonActions.press_key(filename, device, "DPAD_RIGHT", 2, "Right key: Moving right to next card")
            CardCount += 1
        commonActions.press_key(filename, device, "DPAD_DOWN", 2, "Down key: Moving to next row")
    MonkeyRunner.sleep(2)

    print("Successfully navigated,selected and closed all available services in Settings screen")
    device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
    print("Airtel Home button is pressed")
    commonActions.log(filename, device)  # Write logs
    print("end of script")
