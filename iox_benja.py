# THis program is an automated installer for the Cisco Iox client software.
# This program is for windows only. It uses args to run command line commands.
# Variables:
#  - ap_profile: the name of the profile to be created
#  - ap_ip: the ip address of the profile
#  - ap_username: the username of the profile
#  - ap_password: the password of the profile
#  - ap_image_path: a .tar file containing the Iox client software
#  - ap_activation: a json file containing the activation key
# The program reads these variables from an excel or csv file.
# The program will create a profile for each row in the excel file.

import time
import concurrent.futures as cf
import subprocess
from read_csv import read_csv
from generate_ini import *
from confirm_before_run import *
from util import *
from iox_tools import *
# A function to get current working directory.

introduction = """
This program is an automated installer for the Cisco Iox client software.

\033[4mCode written by: Oliver Pan, 2022\033[0m
"""


def main():
    args = get_args()
    program_path = get_cwd()
    csv_path = args.csv
    ap_profile = args.profile
    ap_ip = args.ip
    ap_username = args.username
    ap_password = args.password
    ap_image_path = args.image
    ap_activation = args.activation
    server_ip = args.server
    install_mode = args.mode
    debug_enabled = args.debug
    install_type = None
    if csv_path is None and ap_profile is not None and ap_ip is not None and ap_username is not None and ap_password is not None:
        install_type = "single"
    else:
        install_type = "csv"
    # introduction
    print(introduction)
    iox_version = get_iox_version()
    if iox_version == "0.0.0":
        debug_print(
            "Iox version is not detected, possibly in the init state or incompatible version", debug_enabled)
        debug_print("Trying init config...", debug_enabled)
        color_text(
            f"Please complete the initialization dialog in the Iox client software.", bcolors.WARNING)
        color_text("You can skip the dialog by pressing 'Enter'",
                   bcolors.OKCYAN)
        subprocess.call(f"{program_path} profiles list", shell=True)

    debug_print("install_type: " + install_type, debug_enabled)
    # If the csv file is not provided, the program will use the rest of the variables.
    # Else, the program will use the variables from the csv file.
    # Perform profile creatino if install_mode is "full" or "create"
    if install_mode == "full" or install_mode == "create":
        start_iox_profile(install_type, csv_path, ap_profile,
                          ap_ip, ap_username, ap_password, debug_enabled)

    if install_mode == "delete":  # delete iox profile
        delete_iox_profile(install_type, csv_path, ap_profile)
        return
    if install_mode == "init":  # initialize the program
        init_iox()
    if install_mode == "create":
        color_text("Exiting program...", bcolors.OKCYAN)
        return
    elif install_type == 'single' and (ap_image_path is None or ap_activation is None):
        color_text(
            "No image or activation key provided. Exiting program...", bcolors.OKCYAN)
        return
    # MAIN PROGRAM
    else:
        if install_type == "single":
            if install_mode == "install":
                color_text("Installing Iox client software...",
                           bcolors.OKGREEN)
                print(f'Generating file package_config_{ap_ip}.ini...\n')
                start_iox_install(ap_profile, ap_ip, ap_image_path,
                                  ap_activation, server_ip)
            elif install_mode == "uninstall":
                uninstall_iox(ap_profile)
            elif install_mode == "status":
                check_iox_status(ap_profile)
            elif install_mode == "list":
                check_iox_list(ap_profile)
            elif install_mode == "start":
                start_iox_app(ap_profile)
            elif install_mode == "stop":
                stop_iox_app(ap_profile)
            elif install_mode == "profiles":
                show_profiles()
        else:
            if csv_path is None:
                csv_path = "iox_install.csv"
            df = read_csv(csv_path)
            with cf.ThreadPoolExecutor(max_workers=len(df)) as executor:
                if install_mode == "full" or install_mode == "install":  # perform iox installation
                    color_text("Installing Iox client software...\n",
                               bcolors.OKGREEN)
                    executor.map(
                        start_iox_install, df['profile'], df['ip'], df['image'], df['activation'], df['server'])
                elif install_mode == "uninstall":  # perform iox uninstallation
                    color_text("Uninstalling Iox...\n", bcolors.OKCYAN)
                    executor.map(uninstall_iox, df['profile'])
                elif install_mode == "status":  # show iox status
                    color_text(
                        "Checking status of Iox client software...\n", bcolors.OKGREEN)
                    executor.map(check_iox_status, df['profile'])
                elif install_mode == "list":  # show iox list with installed apps
                    color_text(
                        "Listing installed apps...\n", bcolors.OKGREEN)
                    executor.map(check_iox_list, df['profile'])
                elif install_mode == "start":  # start iox app
                    color_text("Starting Iox client software...\n",
                               bcolors.OKGREEN)
                    executor.map(start_iox_app, df['profile'])
                elif install_mode == "stop":  # start iox app
                    color_text("Stoping Iox client software...\n",
                               bcolors.OKGREEN)
                    executor.map(stop_iox_app, df['profile'])
                elif install_mode == "profiles":  # show iox profiles
                    color_text("Listing profiles...\n",
                               bcolors.OKGREEN)
                    show_profiles()


if confirm_before_run():
    start = time.perf_counter()
    main()
    finish = time.perf_counter()
    color_text(
        f"\n🚀Total time: {round(finish - start, 2)} seconds🚀\n", bcolors.OKGREEN)
else:
    color_text("\nExiting...", bcolors.FAIL)
