import subprocess
import sys
import os


def getTotalNumberOf(filter, filename):
    result = ''
    try:
        command = "grep -oi '" + filter + "' {} | wc -l".format(filename)
        output = subprocess.check_output(command, shell=True)
        result = output.decode().strip()
    except Exception as e:
        print("Exception found as " + e)
    return result


def getDump(filter, filename):
    result = ''
    try:
        command = "grep -niA10 -e '" + filter + "' {}".format(filename)
        output = subprocess.check_output(command, shell=True)
        result = output.decode().strip()
    except Exception as e:
        print("Exception found as " + e)
    return result


def storeIntoReport(filter, filename):
    html_file = ''
    try:
        beginning_of_crash = getTotalNumberOf(filter, filename)
        fatal_exception = getTotalNumberOf('FATAL EXCEPTION', filename)
        table_data = ""

        if int(beginning_of_crash) > 0:
            text = getDump(filter, filename)
            delimiter = "\n--\n"
            # delimiter = "\n"
            items = text.split(delimiter)
            for item in items:
                table_data += '<tr><td colspan="1">' + item + '</th><tr>'
        else:
            table_data = ''

        html_body = '<!DOCTYPE html><html><head><style>table, th, td { border: 2px solid black;}</style></head><body><h2>Crashes</h2><table style="width:20%"><tr><th>Crash Type</th><th>Total</th> </tr><tr><td>Beginning Of Crashes</td><td>' + beginning_of_crash + '</td></tr><tr><td>FATAL EXCEPTION</td><td>' + fatal_exception + '</td></tr></table><table style="width:100%">' + table_data + '</table></body></html>'

        reports_folder = './reports'
        os.makedirs(reports_folder, exist_ok=True)

        html_file = os.path.join(reports_folder, os.path.basename(filename)[:-4] + '.html')

        with open(html_file, 'w') as file:
            file.write(html_body)
    except Exception as e:
        print("Exception found as " + e)
    return html_file
