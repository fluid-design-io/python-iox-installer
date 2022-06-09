import argparse


def get_args():
    parser = argparse.ArgumentParser(
        description="This program is an automated installer for the Cisco Iox client software.")
    parser.add_argument(
        '-c', '--csv', help='The csv file containing the variables.')
    parser.add_argument("-p", "--profile", required=False,
                        help="The name of the profile to be created")
    parser.add_argument("-ip", "--ip", required=False,
                        help="The ip address of the profile")
    parser.add_argument("-u", "--username", required=False, default="admin",
                        help="The username of the profile")
    parser.add_argument("-pass", "--password", required=False,
                        help="The password of the profile")
    parser.add_argument("-i", "--image", required=False,
                        help="A .tar file containing the Iox client software")
    parser.add_argument("-a", "--activation", required=False, default="activation.json",
                        help="A json file containing the activation key")
    parser.add_argument("-m", "--mode", required=False, default="full",
                        choices=["full", "create", "install", "status", "start", "stop", "uninstall", "list", "delete", "profiles"],   help="""
                        The mode of the program.
                        full: create profile, install, start the client. SSH to the AP and enable USB.
                        create: create profile.
                        install: install the client.
                        start: start the client.
                        stop: stop the client.
                        status: check the status of the client.
                        uninstall: uninstall the client.
                        list: list all the apps and states installed on the client.
                        delete: delete the profile.
                        profiles: list all the profiles.
                        """)
    args = parser.parse_args()
    return args
