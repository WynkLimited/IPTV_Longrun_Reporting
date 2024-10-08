from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import sys
import os
import time
import signal
from longrunscripts import commonActions

"""
*Starts recording - records few min - stops recording-plays live for 1hr -schedules reminder - cancel reminder-
navigation in settings screen for 10 min -plays live for 30 min - channel zap forwrd direction

Script functionality
1. Airtel Home 
2. Live
3. Press option btn 
4. selects and clicks on Recording Option
5. recording continues for given time(20 min)
6. navigate through zap banner and stop recording
7. after provided time interval of recording stop the loop will continue again from Airtel home.
8. Tune to LIVE - 1 hr 
9. Airtel Home 
10. Live 
11. Navigate to future event 
12 click on option key 
13. Navigate to Reminder  option ( to schedule reminder) and clik ok to schdule a reminder .
14. after few min/sec  (before scheduled reminder start ) activate zap banner by pressing down key ,
15. navigate to  future event (which was scheduled to remind)
16. click option key 
17. move to reminder option ( to cancel the scheduled reminder) and click on it , scheduled Reminder  is canceled
18. Navigation in settings menu 
19.tune to live channel 
20. channel zap
21. whole loop continues from step 1 to step 20 infinitely till forced to stop.
"""

if len(sys.argv) > 1:
    device_ip = sys.argv[1]
else:
    print("please specify a device")
    sys.exit(1)


# def create_folder_if_not_exists(foldername):
#     folder_path = "./logs/"+foldername
#     if not os.path.exists(folder_path):
# 	print ("folder_path while creating folder " + folder_path)
#         os.makedirs(folder_path)

def exitGracefully(self, signum, frame):
    signal.signal(signal.SIGINT, signal.getsignal(signal.SIGINT))
    device.shell('killall com.android.commands.monkey')
    sys.exit(1)


# append logs
# def log(fn, device):
#     msg = device.shell('logcat -d')
#     f_log = open(fn, 'at')
#     if msg is None:
#         msg = 'None'
#     f_log.write(msg.encode('utf-8'))
#     f_log.close()
#     device.shell('logcat -c')


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

MonkeyRunner.sleep(2)
device.press("BACK", MonkeyDevice.DOWN_AND_UP)
MonkeyRunner.sleep(2)

commonActions.create_folder_if_not_exists(device_ip[0:-5])
folder_path = os.getcwd()
current_file_path = os.path.abspath(__file__)
current_file_name = os.path.basename(current_file_path)
# print ("folder_path " + folder_path +"\n"+ "file" + __file__ + "\n current_file_path " + current_file_path + "\n current_file_name" + current_file_name)

filename = folder_path + '/logs/' + device_ip[0:-5] + '/' + current_file_name[0:-3] + time.strftime(
    "%Y%m%d%H%M%S") + ".log"

while 1:

    # selecting Airtel Home
    device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
    print("Pressed on Airtel Home")
    commonActions.log(filename, device)  # Write logs
    device.shell('logcat -c')  # Clear logs buffer
    MonkeyRunner.sleep(3)

    # Launching LIVE
    device.press("170", MonkeyDevice.DOWN_AND_UP)
    print("Pressed Live Button")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(3)

    # Clicking on Option Button
    device.press("82", MonkeyDevice.DOWN_AND_UP)
    print("Pressed on Option Key")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(3)

    device.press("DPAD_RIGHT", MonkeyDevice.DOWN_AND_UP)
    print("Moving right to select record Option")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(2)

    device.press("DPAD_CENTER", MonkeyDevice.DOWN_AND_UP)
    print("Pressed Ok, Recording Started")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(50)

    device.press("DPAD_DOWN", MonkeyDevice.DOWN_AND_UP)
    print("Activated Zap Banner")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(2)

    # Clicking on Option Button again to stop recording
    device.press("82", MonkeyDevice.DOWN_AND_UP)
    print("Pressed on Option Key")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(3)

    # Recording stopping activity
    device.press("DPAD_RIGHT", MonkeyDevice.DOWN_AND_UP)
    print("Moving right to select record Option")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(2)

    device.press("DPAD_CENTER", MonkeyDevice.DOWN_AND_UP)
    print("Pressed on recording option to stop recording")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(3)

    # closing Recording Stop/continue POP UP
    device.press("DPAD_RIGHT", MonkeyDevice.DOWN_AND_UP)
    print("Moving right to select record Stop Option")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(2)

    device.press("DPAD_CENTER", MonkeyDevice.DOWN_AND_UP)
    print("Pressed Ok, Recording Stopped/Canceled")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(10)

    # Launching LIVE
    device.press("170", MonkeyDevice.DOWN_AND_UP)
    print("Pressed Live Button")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(3600)

    # selecting Airtel Home
    device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
    print("Pressed on Airtel Home")
    commonActions.log(filename, device)  # Write logs
    device.shell('logcat -c')  # Clear logs buffer
    MonkeyRunner.sleep(3)

    # Launching LIVE
    device.press("170", MonkeyDevice.DOWN_AND_UP)
    print("Pressed Live Button")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(3)

    # Navigating to Future event
    device.press("DPAD_DOWN", MonkeyDevice.DOWN_AND_UP)
    print("Navigating to Future event")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(3)

    # Clicking on Option Button
    device.press("82", MonkeyDevice.DOWN_AND_UP)
    print("Pressed on Option Key")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(3)

    device.press("DPAD_RIGHT", MonkeyDevice.DOWN_AND_UP)
    # MonkeyRunner.sleep(2)
    # device.press("DPAD_RIGHT", MonkeyDevice.DOWN_AND_UP)
    print("Moving right to select Reminder Option- To schedule Reminder")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(2)

    device.press("DPAD_CENTER", MonkeyDevice.DOWN_AND_UP)
    print("Pressed Ok, Reminder Scheduled")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(20)

    # Scheduled Reminder cancel activity

    device.press("DPAD_DOWN", MonkeyDevice.DOWN_AND_UP)
    print("Activated Zap Banner")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(2)

    # navigating to future event
    device.press("DPAD_DOWN", MonkeyDevice.DOWN_AND_UP)
    print("Navigating to furure event- which is scheduled for recording")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(2)

    # Clicking on Option Button again to stop Scheduled Reminder
    device.press("82", MonkeyDevice.DOWN_AND_UP)
    print("Pressed on Option Key")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(3)

    # Recording stopping activity
    device.press("DPAD_RIGHT", MonkeyDevice.DOWN_AND_UP)
    # MonkeyRunner.sleep(2)
    # device.press("DPAD_RIGHT", MonkeyDevice.DOWN_AND_UP)
    print("Moving right to select reminder Option(To cancel schedule)")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(2)

    device.press("DPAD_CENTER", MonkeyDevice.DOWN_AND_UP)
    print("Pressed on reminder option to Cancel scheduled reminder-scheduled reminder canceled")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(10)

    # Variables
    menu_count = 8
    time_to_wait = 60 * 10
    timeout = time.time() + time_to_wait
    NoOfRows = 5

    while time.time() < timeout:

        # Launch Airtel home page
        device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
        print("Airtel Home button is pressed")
        commonActions.log(filename, device)  # Write logs
        MonkeyRunner.sleep(2)

        # Navigating to Settings menu in Airtel home screen
        for i in range(1, menu_count):
            device.press("DPAD_RIGHT", MonkeyDevice.DOWN_AND_UP)
            print("Pressed RIGHT key %d time to navigate to Settings menu in Airtel home screen" % i)
            commonActions.log(filename, device)  # Write logs
            MonkeyRunner.sleep(1)

        MonkeyRunner.sleep(5)
        # Selecting Settings in Menu
        device.press("DPAD_CENTER", MonkeyDevice.DOWN_AND_UP)
        print("Selection key is pressed on Settings")
        commonActions.log(filename, device)  # Write logs
        MonkeyRunner.sleep(3)

        # Navigate across all the cards under Settings screen
        for row in range(NoOfRows):
            CardCount = 0
            while CardCount < 4:
                device.press("DPAD_RIGHT", MonkeyDevice.DOWN_AND_UP)
                print("Right key: Moving right to next card")
                MonkeyRunner.sleep(2)
                commonActions.log(filename, device)  # Write logs
                MonkeyRunner.sleep(2)
                CardCount += 1

            device.press("DPAD_DOWN", MonkeyDevice.DOWN_AND_UP)
            print("Down key: Moving to next row")
            MonkeyRunner.sleep(2)
            commonActions.log(filename, device)  # Write logs
        MonkeyRunner.sleep(5)

    # Navigating to LIVE
    device.press("170", MonkeyDevice.DOWN_AND_UP)
    print("LIVE Button is pressed")
    commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(1800)

    Chforward = 15
    # Channel change key forward movement
    for i in range(1, Chforward):
        device.press("CHANNEL_UP", MonkeyDevice.DOWN_AND_UP)
        print("Pressed channel up key for %d time" % i)
        MonkeyRunner.sleep(5)
        commonActions.log(filename, device)  # Write logs
    MonkeyRunner.sleep(7)
