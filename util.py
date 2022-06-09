import os
import time
import subprocess


def execute_command(ps, command, sleep=0.03):
    time.sleep(sleep)
    ps.stdin.write(command.encode())


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# A function to print colored text using bcolors class, takes in a string and a color from the bcolors class.


def color_text(text, color):
    print(color + text + bcolors.ENDC)


def get_cwd(path='ioxclient'):
    cwd = os.getcwd()
    if path:
        cwd = os. path.join(cwd, path)
    # replace " " with "\\ "
    return cwd.replace(" ", "\\ ")

# A function make this command used many times: subprocess.Popen(f'.\\ioxclient.exe --profile {ap_profile} app install iox_benja .\\{ap_image_path}', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def run_terminal(cmd):
    ps = subprocess.Popen(cmd, shell=True,
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return ps
