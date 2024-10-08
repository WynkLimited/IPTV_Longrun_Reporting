import os
import subprocess
import glob
import sys
import pandas as pd
from datetime import datetime
from find_crash import storeIntoReport
import re
import webbrowser
from concurrent.futures import ThreadPoolExecutor, as_completed


def getTotalNumberOf(filter, filename):
    result = ''
    try:
        command = "grep -oi '" + filter + "' {} | wc -l".format(filename)
        output = subprocess.check_output(command, shell=True)
        result = output.decode().strip()
    except Exception as e:
        print("Exception found as " + e)
    return result


def getTotalTimeRan(filename):
    diff = 0.0
    try:
        command = 'grep -oE "^.{16}" ' + filename
        output = subprocess.check_output(command, shell=True)
        result = output.decode().splitlines()
        pattern = r"\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d"
        matches = [elem for elem in result if re.match(pattern, elem)]
        timestamp1 = matches[0]
        timestamp2 = matches[-1]
        format = "%m-%d %H:%M:%S.%f"
        dt1 = datetime.strptime(timestamp1, format)
        dt2 = datetime.strptime(timestamp2, format)
        diff = (dt2 - dt1)
    except:
        print('exception found for ', filename)
    return (diff)


def pushToFile(content):
    try:
        with open("report.txt", "a") as file:
            file.write('\n')
            current_datetime = datetime.now()
            file.write(str(current_datetime))
            file.write('\n')
            file.write(content)
            file.write('\n')
            file.write('##################################################################')
            file.write('\n')
    except Exception as e:
        print("Exception found as " + e)


def get_text_files(directory):
    text_files = []
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".log"):
                    text_files.append(os.path.join(root, file))
    except Exception as e:
        print("Exception found as " + e)
    return text_files


def get_latest_file(directory):
    recent_files = []
    try:
        for dirpath, dirnames, filenames in os.walk(directory):
            txt_files = glob.glob(os.path.join(dirpath, "*.log"))
            if txt_files:
                most_recent_file = max(txt_files, key=os.path.getctime)
                recent_files.append(most_recent_file)
    except Exception as e:
        print("Exception found as " + e)
    return recent_files


def fileCreatedTimeStamp(file):
    return os.path.getctime(file)


def process_file(file):
    current_directory = os.getcwd()
    file_name = file.replace(current_directory + '/', '')
    data = getTotalNumberOf(' beginning of crash', file)
    time_difference = getTotalTimeRan(file)
    html_file = storeIntoReport(' beginning of crash', file)

    return {'file_name': file_name, 'time_difference': time_difference, 'data': data, 'html_file': html_file}


def process_data():
    CURRENT_DASHBOARD = {'SL.NO': [], 'FILE_NAME': [], 'RAN_FOR': [], 'CRASHES': [], 'REPORT': []}
    current_directory = os.getcwd()
    if len(sys.argv) > 1:
        txt_files = get_text_files(current_directory)
    else:
        txt_files = get_latest_file(current_directory)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_file, file) for file in txt_files]

        for index, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            CURRENT_DASHBOARD['SL.NO'].append(index)
            CURRENT_DASHBOARD['FILE_NAME'].append(result['file_name'])
            CURRENT_DASHBOARD['RAN_FOR'].append(result['time_difference'])
            CURRENT_DASHBOARD['CRASHES'].append(result['data'])
            CURRENT_DASHBOARD['REPORT'].append(result['html_file'])

    html_content = "<html>\n<head>\n<style>\ntable {\nborder-collapse: collapse;\nwidth: auto;\n}\nth, td {\npadding: 8px;\ntext-align: left;\nborder-bottom: 1px solid #ddd;\n}\nth {\nbackground-color: #f2f2f2;\ntext-align: center;\n}\na.button {\ndisplay: inline-block;\nbackground-color: #4CAF50;\ncolor: white;\npadding: 8px 16px;\ntext-align: center;\ntext-decoration: none;\n}\na.button:hover {\nbackground-color: #45a049;\n}\nh1 {\ntext-align: center;\n}\n</style>\n</head>\n<body>\n<h1>Airtel DTH Longrun Report</h1>\n<table>\n<tr>\n<th>SL.NO</th>\n<th>FILE_NAME</th>\n<th>RAN_FOR</th>\n<th>CRASHES</th>\n<th>REPORT</th>\n</tr>\n"

    for index in range(len(CURRENT_DASHBOARD['SL.NO'])):
        file_name = CURRENT_DASHBOARD['FILE_NAME'][index]
        ran_for = CURRENT_DASHBOARD['RAN_FOR'][index]
        crashes = CURRENT_DASHBOARD['CRASHES'][index]
        report = CURRENT_DASHBOARD['REPORT'][index]

        html_content += f"<tr>\n<td>{index + 1}</td>\n<td>{file_name}</td>\n<td>{ran_for}</td>\n<td>{crashes}</td>\n<td><a class='button' href='{report}' target='_blank'>Open</a></td>\n</tr>\n"

    html_content += "</table>\n</body>\n</html>"

    with open('index.html', 'w') as file:
        file.write(html_content)


try:
    process_data()
finally:
    url = "http://127.0.0.1:8080/"
    webbrowser.open(url)
