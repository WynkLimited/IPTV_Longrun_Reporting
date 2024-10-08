import os


def get_the_latest_pids():
    filename = './files/pids.txt'
    with open(filename, 'r') as file:
        lines = file.readlines()
    latest_pids = lines[-1].strip()
    return eval(latest_pids)


processes = get_the_latest_pids()
pids = list(processes.values())
kill_command = ['kill'] + [str(pid) for pid in pids]
os.system(' '.join(kill_command))
