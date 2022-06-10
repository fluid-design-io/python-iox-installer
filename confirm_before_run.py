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
    # if csv is not provided, the program will use the rest of the variables.
    if args.csv is None and args.profile is not None and args.ip is not None and args.username is not None and args.password is not None:
        color_text(
            f"\n🚀Running Iox client software for {args.profile}🚀\n", bcolors.HEADER)
        color_text(
            "This feature is not yet implemented. Exiting program...", bcolors.OKCYAN)
        return False
    else:
        csv = "iox_install.csv" if args.csv is None else args.csv
        color_text(
            f"\n🚀Running Iox client software for {csv}🚀\n", bcolors.HEADER)
    if args.mode == "full" or args.mode == "create":
        # confirm before running, if user enter "n" or "N", exit the program
        return confirm_input('Are you sure you want to install Iox client software?')
    if args.mode == "install" or args.mode == "uninstall" or args.mode == "start" or args.mode == "stop":
        return confirm_input(
            f"Are you sure you want to {args.mode} Iox client software?")
    if args.mode == "delete":
        return confirm_input(f"Are you sure you want to delete profile(s)")
    if args.mode == "init":
        return confirm_input(f"Note: this is only used the first time you run the program. Are you sure you want to initialize the program?")
    if args.mode == "status" or args.mode == "list" or args.mode == "profiles":
        return True
