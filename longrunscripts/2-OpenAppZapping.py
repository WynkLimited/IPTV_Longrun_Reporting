from com.android.monkeyrunner import MonkeyRunner
import sys
import os
import time
import signal

import commonActions

try:

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
    Main_menu_count = 8
    RowsBetweenBanners = 3

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
        try:

            commonActions.click_home(filename, device, 15)

            for l in range(0, 7):
                commonActions.continue_press(filename, device, "DPAD_DOWN", 2)
                commonActions.continue_press(filename, device, "DPAD_RIGHT", l)
                commonActions.press_key(filename, device, "DPAD_CENTER", 1, "Selection key is pressed")
                commonActions.continue_press(filename, device, "DPAD_DOWN", 2)
                commonActions.click_home(filename, device, 15)

        except Exception:
            print("******* final catch *******")
            break

    print("Successfully navigated to all available menu list in Airtel Home")
    commonActions.click_home(filename, device, 15)
    print("end of script")
except:
    print("Stopped")
    sys.exit(1)
