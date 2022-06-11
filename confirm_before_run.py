from util import *
from get_args import get_args

# a function that prompt user to enter yes or no, takes an argument of the question


def confirm_input(message):
    while True:
        color_text(message, bcolors.BOLD)
        color_text("(y/n)", bcolors.OKCYAN)
        choice = input("\n")
        if choice == "y" or choice == "Y":
            return True
        elif choice == "n" or choice == "N":
            return False
        else:
            color_text("Please enter y or n", bcolors.FAIL)


def confirm_before_run():
    args = get_args()
    install_mode = args.mode
    # if csv is not provided, the program will use the rest of the variables.
    if args.csv is None and args.profile is not None and args.ip is not None and args.username is not None and args.password is not None:
        if install_mode == "create":
            # check if variables for install mode is provided
            if args.image is None or args.activation is None or args.server is None:
                return color_text(
                    "Please provide all the necessary variables for the full installation.", bcolors.FAIL)

            else:
                # confirm before running the program
                return confirm_input(f"Are you sure you want to {args.mode} {args.profile}?")
        if install_mode == "delete":
            # check if all the variables are provided
            if args.profile is None:
                color_text(
                    "Please provide the profile name to be deleted.", bcolors.FAIL)
                return
            else:
                return confirm_input(f"Are you sure you want to delete {args.profile} profile?")
    else:
        csv = "iox_install.csv" if args.csv is None else args.csv
        color_text(
            f"\n🚀Running Iox client software for {csv}🚀\n", bcolors.HEADER)
    if install_mode == "full" or install_mode == "create":
        # confirm before running, if user enter "n" or "N", exit the program
        m = "full install" if install_mode == "full" else "create profile"
        return confirm_input(f'Are you sure you want to {m} Iox client software?')
    if install_mode == "install" or install_mode == "uninstall" or install_mode == "start" or install_mode == "stop":
        return confirm_input(
            f"Are you sure you want to {install_mode} Iox client software?")
    if install_mode == "delete":
        return confirm_input(f"Are you sure you want to delete profile(s)")
    if install_mode == "init":
        return confirm_input(f"Note: this is only used the first time you run the program. Are you sure you want to initialize the program?")
    if install_mode == "status" or install_mode == "list" or install_mode == "profiles":
        return True
