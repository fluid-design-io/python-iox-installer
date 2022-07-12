import argparse
import settings


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
                        help="The password of the profile"),
    parser.add_argument("-s", "--secret", required=False,
                        help="The enable secret of the profile"),
    parser.add_argument("-i", "--image", required=False,
                        help="A .tar file containing the Iox client software")
    parser.add_argument("-a", "--activation", required=False, default="activation.json",
                        help="A json file containing the activation key")
    parser.add_argument("-S", "--server", required=False,
                        help="The ip address of the server, used when generating package_config.ini")
    parser.add_argument("-m", "--mode", required=False, default="full",
                        choices=["full", "create", "install", "status", "start", "stop", "uninstall", "list", "delete", "profiles", "init"],   help="""
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
                        init: initialize the program. skip the day0 dialog with empty info.
                        """)
    parser.add_argument("-d", "--debug", required=False,
                        action="store_true", help="Debug mode")
    # add a version flag
    parser.add_argument("-v", "--version", action="version",
                        version="%(prog)s 1.5.0")
    # add a language flag, supports English and Korean
    parser.add_argument("-l", "--language", required=False, default="en",
                        choices=["en", "ko"],
                        help="The language of the program.")
    args = parser.parse_args()
    # Set settings
    settings.language = args.language
    settings.debug = args.debug
    return args

    # Make a markdown table for the arguments


table = """
| Argument | Value | Description | Required | Default | Type |
| -------- | ---- | ----------- | -------- | ------- | ---- |
| -c, --csv | csv_path | The csv file containing the variables. | Yes | None | str |
| -p, --profile | ap_profile | The name of the profile to be created | No | None | str |
| -ip, --ip | ap_ip | The ip address of the profile | No | None | str |
| -u, --username | ap_username | The username of the profile | No | admin | str |
| -pass, --password | ap_password | The password of the profile | No | None | str |
| -s, --secret | ap_secret | The enable secret of the profile | No | None | str |
| -i, --image | image_path | A .tar file containing the Iox client software | No | None | str |
| -a, --activation | activation_path | A json file containing the activation key | No | activation.json | str |
| -S, --server | server_ip | The ip address of the server, used when generating package_config.ini | No | None | str |
| -m, --mode | mode | The mode of the program. | Yes | full | str |
| -d, --debug | debug | Debug mode | No | False | bool |
| -v, --version | version | Version | No | False | bool |
| -l, --language | language | The language of the program. | No | en | str |
"""
