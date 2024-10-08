import os
import subprocess
import glob
import sys
import pandas as pd
from tabulate import tabulate
from datetime import datetime
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

global_file_sizes = {}

def getTotalNumberOf(filter, filename):
    result = ''
    try:
        command = "grep -oi '"+filter+"' {} | wc -l".format(filename)
        output = subprocess.check_output(command, shell=True)
        result = output.decode().strip()
    except Exception as e:
        print("Exception found as "+e)
    return result

def getTotalTimeRan(filename):
    diff = 0.0
    try:
        command = 'grep -oE "^.{16}" '+filename
        output = subprocess.check_output(command, shell=True)
        result = output.decode().splitlines()
        pattern = r"\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d"
        matches = [elem for elem in result if re.match(pattern, elem)]
        timestamp1 = matches[0]
        timestamp2 = matches[-1]
        format = "%m-%d %H:%M:%S.%f"
        dt1 = datetime.strptime(timestamp1, format)
        dt2 = datetime.strptime(timestamp2, format)
        diff = dt2 - dt1
    except:
        print('exception found for ',filename)
    return (diff)

def pushToFile(content):
    try:
        with open("./files/report.txt", "a") as file:
            file.write('\n')
            current_datetime = datetime.now()
            file.write(str(current_datetime))
            file.write('\n')
            file.write(content)
            file.write('\n')
            file.write('##################################################################')
            file.write('\n')
    except Exception as e:
        print("Exception found as "+e)

def get_text_files(directory):
    text_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".log"):
                text_files.append(os.path.join(root, file))
    return text_files

def get_latest_file(directory):
    recent_files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        txt_files = glob.glob(os.path.join(dirpath, "*.log"))
        if txt_files:
            most_recent_file = max(txt_files, key=os.path.getctime)
            recent_files.append(most_recent_file)
    return recent_files

def isTheFileSizeIncreasing(file_path, initial_size):
    current_size = os.path.getsize(file_path)
    if current_size > initial_size:
        return 'Running'
    else:
        return ''

def getInitialSize(file):
    try:
        return global_file_sizes[file]
    except:
        return 0

def setInitialSize(file):
    global_file_sizes[file] = os.path.getsize(file)

def fileCreatedTimeStamp(file):
    return os.path.getctime(file)

def process_file(file):
    current_directory = os.getcwd()
    file_name = file.replace(current_directory+'/', '')
    data = getTotalNumberOf(' beginning of crash', file)
    status = isTheFileSizeIncreasing(file, getInitialSize(file))
    time_difference = getTotalTimeRan(file)
    setInitialSize(file)
    return {'file_name': file_name, 'time_difference': time_difference, 'status': status, 'data': data}

def process_data():
    total_crashes = 0
    total_run_time = 0.0
    CURRENT_DASHBOARD = {'FILE_NAME':[], 'RAN_FOR':[], 'STATUS':[], 'CRASHES':[]}
    current_directory = os.getcwd()
    if len(sys.argv) > 1:
        txt_files = get_text_files(current_directory)
    else:
        txt_files = get_latest_file(current_directory)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_file, file) for file in txt_files]

        for future in as_completed(futures):
            result = future.result()
            CURRENT_DASHBOARD['FILE_NAME'].append(result['file_name'])
            CURRENT_DASHBOARD['RAN_FOR'].append(result['time_difference'])
            CURRENT_DASHBOARD['STATUS'].append(result['status'])
            CURRENT_DASHBOARD['CRASHES'].append(result['data'])
            total_crashes += int(result['data'])
            total_run_time += result['time_difference'].total_seconds()

    df = pd.DataFrame(CURRENT_DASHBOARD)
    df.index = df.reset_index().index + 1
    
    total_run_time_hours = total_run_time / 3600

    total_row = pd.DataFrame({'FILE_NAME': ['Total'], 'RAN_FOR': [f'{total_run_time_hours:.2f} hours'], 'STATUS': [''], 'CRASHES': [total_crashes]})
    df = pd.concat([df, total_row], ignore_index=True)
    df.iloc[-1, 0] = ''

    print('\n')
    print('##################################################################')
    print(str(datetime.now()))
    print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
    pushToFile(tabulate(df, headers='keys', tablefmt='fancy_grid'))

while True:
    process_data()
    time.sleep(5)