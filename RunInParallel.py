import subprocess
import psutil
import configparser
import time

data = []
subprocesses = {}

config = configparser.ConfigParser()
config.read('./files/deviceconfig.properties')

def check_pid_running(pid):
    return psutil.pid_exists(pid)

def get_the_latest_pids():
    latest_pids = '{}'
    filename = './files/pids.txt'
    with open(filename, 'r') as file:
        lines = file.readlines()
    if(len(lines))>0:
        latest_pids = lines[-1].strip()
    return eval(latest_pids)

existing = get_the_latest_pids()

for section in config.sections():
    script_file = config.get(section, 'script_file')
    deviceip = config.get(section, 'deviceip')
    data.append((script_file, deviceip))

def writeIntoFile(content):
    with open('./files/pids.txt', 'a') as file:
        file.write(str(content) + '\n')

def writeFirst(content):
    file_path = './files/pids.txt'
    with open(file_path, 'r') as file:
        existing_content = file.read()
    with open(file_path, 'w') as file:
        file.write(str(content) + '\n')
        file.write(existing_content)

def process_data(script_file, deviceip):
    # cmd = ['python3', script_file, deviceip]
    cmd = ['monkeyrunner', script_file, deviceip]
    if deviceip in existing:
        if not check_pid_running(existing[deviceip]):
            process = subprocess.Popen(cmd)
            subprocesses.setdefault(deviceip, process.pid)
        else:
            subprocesses.setdefault(deviceip, existing[deviceip])
    else:
        process = subprocess.Popen(cmd)
        subprocesses.setdefault(deviceip, process.pid)

try:
    for item in data:
        script_file = item[0]
        deviceip = item[1]
        time.sleep(1)
        process_data(script_file, deviceip)
        time.sleep(1)
except Exception as e:
    print("Exception found due to "+e)
finally:
    writeIntoFile(subprocesses)