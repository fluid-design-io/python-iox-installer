import io
import os
import json
import time
import subprocess
import settings


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


def debug_print(text, enabled=False, ps=None):
    if enabled:
        if ps is not None:
            # ps.stdin.write(text.encode())
            print(text)
        else:
            color_text(text, bcolors.HEADER)


# A function to get current working directory. Returns the path as a string.
def get_cwd(path='ioxclient'):
    cwd = os.getcwd()
    if path:
        cwd = os. path.join(cwd, path)
    # replace " " with "\\ "
    # check if is mac or windows
    if os.name == 'nt':
        cwd = cwd.replace(" ", "\\ ")
    else:
        cwd = cwd.replace(" ", "\ ")
    return cwd


def run_terminal(cmd):
    ps = subprocess.Popen(cmd, shell=True,
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return ps


def read_as_utf8(fileno):
    fp = io.open(fileno, mode="r", encoding="utf-8", closefd=False)
    print(fp.read())
    fp.close()


def versiontuple(v):
    return tuple(map(int, (v.split("."))))


def get_iox_version():
    ps = run_terminal(f'{get_cwd()} --version')
    ps_ver = ps.communicate()[0].decode()
    # Check for iox app permission error
    if ps_ver.find('Permission denied') != -1:
        color_text('ioxclient: Permission denied', bcolors.FAIL)
        return None
    ps_ver = ps_ver.split('\n')
    ps_ver = ps_ver[0].split(' ')
    ps_ver = ps_ver[2]

    if ps_ver == "not":
        ps_ver = "0.0.0"

    return ps_ver


def get_sys_msg(key):
    # Get language from settings.py
    language = settings.language
    # Get the translation file from the language folder inside the locales folder
    translation_file = os.path.join(
        'locales', language, 'translation.json')
    # Read the translation file
    with open(translation_file, 'r') as f:
        translation = json.load(f)
        # Return the translation for the key if it exists, otherwise return the key
        if key in translation:
            return translation[key]
        else:
            return key
