from generate_ini import *
from confirm_before_run import *
from ssh_add_usb_module import ssh_add_usb_module
from util import *
from iox_tools import *
from read_csv import read_csv
from yaspin import yaspin
from yaspin.spinners import Spinners


def create_iox_profile(ap_profile, ap_ip, ap_username, ap_password, debug_enabled=False):
    program_path = get_cwd()
    iox_version = get_iox_version()  # A fix for version incompatibility
    debug_print(f"iox_version: {iox_version}", debug_enabled)

    with yaspin(Spinners.moon, text=f"Creating profile: {ap_profile}") as sp:
        ps = run_terminal(f'{program_path} profiles create')
        debug_print(f"Creating profile", debug_enabled, ps)
        execute_command(ps, ap_profile + "\n", sleep=0.3)  # profile name
        sp.text = f"Creating profile: {ap_profile}"
        execute_command(ps, ap_ip + "\n")  # ip address
        sp.text = f"Creating profile: {ap_ip}"
        execute_command(ps, "\n")  # IOx platform's port [8443]
        execute_command(ps, ap_username + "\n")  # username
        sp.text = f"Creating profile: {ap_username}"
        execute_command(ps, ap_password + "\n")  # password
        sp.text = f"Creating profile: {ap_password}"
        # Local repository path [/software/downloads]
        execute_command(ps, "\n")
        execute_command(ps, '\n')  # Connection Timeout Millisecond [1000]
        execute_command(ps, "\n")  # URL scheme [https]
        # Check for version incompatibility, if version is None, then exit the program
        if iox_version is None:
            color_text(
                f"{get_sys_msg('version_not_found')}", bcolors.FAIL)
            exit(1)
        else:  # Only execute this command if the version is >= 1.16.0.0
            if versiontuple(iox_version) >= versiontuple("1.16.0.0"):
                print(f"versiontuple: {iox_version}")
                execute_command(ps, "\n")  # API Prefix[/iox/api/v2/hosting]
        execute_command(ps, "22\n")  # IOx platform's SSH port [2222]: 22
        sp.text = f"Creating profile: 22"
        execute_command(ps, "\n")  # RSA key, in PEM format
        execute_command(ps, "\n")  # x.509 certificate, in PEM format
        create_res = ps.communicate()[0].decode()
        debug_print(
            f"Closing communication", debug_enabled, create_res)
        if "Error" in create_res:
            sp.text = f"Creating profile: {ap_profile}"
            sp.fail = f"{ap_profile}: Error while creating profile"
            color_text(
                f"\n{ap_profile}: Error while creating profile", bcolors.FAIL)
            print(create_res)
        else:
            sp.text = ""
            sp.ok(f"✅ {ap_profile} created")


def delete_iox_profile(install_type, csv_path, ap_profile):
    program_path = get_cwd()
    if install_type == "single":
        ps = run_terminal(f'{program_path} profiles delete {ap_profile}')
        ps.communicate()[0].decode()
        color_text(f"{ap_profile}: Profile deleted", bcolors.OKGREEN)
    else:
        if csv_path is None:
            csv_path = "iox_install.csv"
        df = read_csv(csv_path)
        with yaspin(Spinners.moon, text=f"Deleting profiles") as sp:
            for index, row in df.iterrows():
                sp.text = f"Deleting profile {row['profile']}"
                ps = run_terminal(
                    f'{program_path} profiles delete {row["profile"]}')
                ps.communicate()[0].decode()
            sp.text = ""
            sp.ok(f"✅ Deleted {len(df)} profiles")
        # print(f"\n🚀{ap_profile} profile deleted🚀\n")


def start_iox_install(ap_profile, ap_ip, ap_image_path, ap_activation, server_ip):
    program_path = get_cwd()
    app_state = check_iox_status(ap_profile, False)
    if app_state == "RUNNING":
        color_text(
            f"{ap_profile}: {get_sys_msg('iox_already_running')}", bcolors.OKGREEN)
        return
    else:
        with yaspin(Spinners.moon, text=f"Generating package_config.ini") as sp:

            config_ini_name = gen_ini(ap_ip, server_ip)

            sp.text = f"Installing Iox client software"
            ps_install = run_terminal(
                f'{program_path} --profile {ap_profile} app install iox_benja {ap_image_path}')

            ps_install.communicate()[0].decode()

            sp.spinner = Spinners.simpleDotsScrolling

            sp.text = f"Activating Iox client software"
            ps_activation = run_terminal(
                f'{program_path} --profile {ap_profile} app activate iox_benja --payload {ap_activation}')
            ps_activation.communicate()[0].decode()

            sp.text = f"Setting package_config.ini"
            ps_config = run_terminal(
                f'{program_path} --profile {ap_profile} app setconfig iox_benja {config_ini_name}')
            config_res = ps_config.communicate()[0].decode()
            if "Error" in config_res:
                err_msg = get_sys_msg("setting_package")
                color_text(
                    f"\n{ap_profile}: {err_msg}", bcolors.FAIL)
                print(config_res)
            # color_text(
            #     f"Starting Iox client software for {ap_profile}", bcolors.OKGREEN)

            sp.text = f"Starting Iox client software"
            start_iox_app(ap_profile)
            check_iox_status(ap_profile)
            # remove the generated ini file
            del_ini(ap_ip, server_ip)


def start_iox_profile(mode, csv_path, ap_profile, ap_ip, ap_username, ap_password, debug_enabled):
    if mode == "single":
        create_iox_profile(ap_profile, ap_ip, ap_username, ap_password)
    else:
        if csv_path is None:
            csv_path = "iox_install.csv"
            debug_print(
                f"csv_path is not provided, using default: {csv_path}", debug_enabled)
        df = read_csv(csv_path)
        debug_print("csv file read", debug_enabled)
        debug_print(f"{len(df)} profiles found", debug_enabled)
        # loop through the csv file and create profiles
        color_text(f"Creating profiles for {len(df)} devices", bcolors.OKGREEN)
        for index, row in df.iterrows():
            create_iox_profile(row['profile'], row['ip'],
                               row['username'], row['password'], debug_enabled)
        color_text(
            f"Added {len(df)} profiles", bcolors.OKGREEN)
        # print out the names of the profiles created.
        # for index, row in df.iterrows():
        #     print(row['profile'], row['ip'])


def start_iox_app(ap_profile, csv_path, ap_ip, ap_username, ap_password, ap_secret, debug_enabled):
    def check_res_has_error(res):
        for line in res:
            if "Error:" in line:
                color_text(f"{ap_profile}: Error", bcolors.FAIL)
            if "description" in line:
                if "/dev/ttyUSB0" in line:
                    color_text(
                        f"{ap_profile}: {get_sys_msg('no_usb_found')}", bcolors.FAIL)
                    return True
                break
        return False

    program_path = get_cwd()
    app_state = check_iox_status(ap_profile, False)

    if app_state == "RUNNING":
        color_text(
            f"{ap_profile}: {get_sys_msg('iox_already_running')}", bcolors.OKGREEN)
        return
    else:
        ps_start = run_terminal(
            f'{program_path} --profile {ap_profile} app start iox_benja')
        res = ps_start.communicate()[0].decode()
        debug_print(f"{ap_profile}: {res}", debug_enabled)
    # res looks like this:
    # Error occured,
    # Currently active profile :  AP-9120-01
    # Command Name:  application-start
    # Error. Server returned 500
    # {
    #  "description": "Error while starting the app: iox_benja, Cause: Failed to start container: Error: internal error: guest failed to start: Unable to access /dev/ttyUSB0: No such file or directory\n",
    #  "errorcode": -1014,
    #  "message": "Error while changing app state"}
    # Activating Profile  AP-9120-01

    # If Error. then print the error message
    res = res.split("\n")
    if check_res_has_error(res):
        debug_print(
            f"{ap_profile}: {get_sys_msg('attemp_ssh_usb')}", debug_enabled)
        ssh_add_usb_module(ap_ip, ap_username, ap_password,
                           ap_secret, debug_enabled)
        debug_print(f"{ap_profile}: Rerunning the command", debug_enabled)
        ps_start = run_terminal(
            f'{program_path} --profile {ap_profile} app start iox_benja')
        res = ps_start.communicate()[0].decode()
        debug_print(f"{ap_profile}: {res}", debug_enabled)


def stop_iox_app(ap_profile):
    program_path = get_cwd()
    ps_stop = run_terminal(
        f"{program_path} --profile {ap_profile} app stop iox_benja")
    ps_stop.communicate()[0].decode()
    color_text(f"{ap_profile} is stopped", bcolors.OKGREEN)


def check_iox_status(ap_profile, show_output=True):
    program_path = get_cwd()
    ps_status = run_terminal(
        f'{program_path} --profile {ap_profile} app status iox_benja')
    res = ps_status.communicate()[0].decode()

    res = res.split('\n')
    for line in res:
        if "RUNNING" in line:
            color_text(f"{ap_profile} is running",
                       bcolors.OKGREEN) if show_output else None
            return "RUNNING"
        elif "STOPPED" in line:
            color_text(f"{ap_profile} is stopped",
                       bcolors.FAIL) if show_output else None
            return "STOPPED"
        elif "ACTIVATED" in line:
            color_text(f"{ap_profile} is activated",
                       bcolors.OKGREEN) if show_output else None
            return "ACTIVATED"
        elif "DEACTIVATED" in line:
            color_text(f"{ap_profile} is deactivated",
                       bcolors.WARNING) if show_output else None
            return "DEACTIVATED"
        elif "not found" in line:
            color_text(f"{ap_profile} is not installed",
                       bcolors.BOLD) if show_output else None
            return "NOT FOUND"
    color_text(
        f"{ap_profile} {get_sys_msg('ap_state_unkown')}", bcolors.FAIL) if show_output else None
    return "ERROR"


def check_iox_list(ap_profile):
    program_path = get_cwd()
    ps_list = run_terminal(
        f'{program_path} --profile {ap_profile} app list')
    res = ps_list.communicate()[0].decode()
    # This is the res looks like:
    # Currently active profile :  AP-9120-01
    # Overriding profile to AP-9120-01 for this command
    # Activating Profile  AP-9120-01
    # Command Name:  application-list
    # List of installed App :
    #  1. iox_benja  --->    RUNNING
    # Activating Profile  AP-9120-01

    # Only show the list of installed app
    isEndCounter = 0
    appCounter = 0
    res = res.split('\n')
    for line in res:
        if "--->" in line:
            appCounter += 1
            print(f'{ap_profile} {line}')
        if "Activating Profile" in line:
            if isEndCounter == 1:
                if appCounter == 0:
                    color_text(
                        f"{ap_profile} have 0 app installed", bcolors.BOLD)
                return
            isEndCounter += 1


def uninstall_iox(ap_profile):
    program_path = get_cwd()
    # ioxclient --profile AP-9120-01 application stop iox_benja && ioxclient --profile AP-9120-01 application deactivate iox_benja && ioxclient --profile AP-9120-01 application uninstall iox_benja
    app_state = check_iox_status(ap_profile, False)

    if app_state == "RUNNING":
        ps_uninstall = run_terminal(
            f'{program_path} --profile {ap_profile} application stop iox_benja && ioxclient --profile {ap_profile} application deactivate iox_benja && ioxclient --profile {ap_profile} application uninstall iox_benja')
    elif app_state == "NOT FOUND":
        color_text(
            f"{ap_profile} {get_sys_msg('iox_not_installed')}", bcolors.BOLD)
        return
    else:
        ps_uninstall = run_terminal(
            f'{program_path} --profile {ap_profile} application deactivate iox_benja && ioxclient --profile {ap_profile} application uninstall iox_benja')

    res = ps_uninstall.communicate()[0].decode()
    # if res contain "Error.", then print the error, else print success
    if "Error." in res:
        color_text(
            f'Error occured,\n{bcolors.ENDC}{bcolors.BOLD}{res}{bcolors.ENDC}', bcolors.FAIL)
    else:
        color_text(
            f'{ap_profile} is uninstalled', bcolors.OKGREEN)


def show_profiles():
    program_path = get_cwd()
    ps_list = run_terminal(
        f'{program_path} profiles list')
    res = ps_list.communicate()[0].decode()
    res = res.split('\n')
    for line in res:
        if "Profile Name" in line:
            color_text(f"Name: {line[16:]}", bcolors.HEADER)
        if "Host IP:" in line:
            color_text(f"IP:   {line[11:]}", bcolors.ENDC)
            print("-" * 40)


def init_iox():
    program_path = get_cwd()
    color_text(program_path, bcolors.WARNING)
    ps_init = run_terminal(
        [f'{program_path} profiles create'])
    read_as_utf8(ps_init.stdout.fileno())
    pipe_r, pipe_w = os.pipe()
    os.write(pipe_w, "Lorem ipsum.".encode("utf-8"))
    os.close(pipe_w)
    read_as_utf8(pipe_r)  # prints "Lorem ipsum."
    os.close(pipe_r)
    color_text(f'{ps_init.communicate[0].decode()}', bcolors.OKGREEN)
