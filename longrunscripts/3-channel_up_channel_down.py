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

MonkeyRunner.sleep(5)
device.press("BACK", MonkeyDevice.DOWN_AND_UP)

commonActions.create_folder_if_not_exists(device_ip[0:-5])
folder_path = os.getcwd()
current_file_path = os.path.abspath(__file__)
current_file_name = os.path.basename(current_file_path)
# print ("folder_path " + folder_path +"\n"+ "file" + __file__ + "\n current_file_path " + current_file_path + "\n current_file_name" + current_file_name)

filename = folder_path + '/logs/' + device_ip[0:-5] + '/' + current_file_name[0:-3] + time.strftime(
    "%Y%m%d%H%M%S") + ".log"
# filename = current_file_name[0:-3]+time.strftime("%Y%m%d%H%M%S") + ".log"

while True:
    # Presses the speaker button
    device.shell("input keyevent 3")
    device.shell("input keyevent 4")
    for l in range(0, 100):
        commonActions.press_key(filename, device, "CHANNEL_UP", 5, "send channel up key")
    for j in range(100, 0, -1):
        commonActions.press_key(filename, device, "CHANNEL_DOWN", 5, "send channel down key")

# print("end of script")
