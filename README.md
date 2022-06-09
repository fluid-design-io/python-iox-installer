# Python IOx Installer

### install multiple iox_benja at once with python threading

# Introduction

This program is an automated installer for the Cisco Iox client software.
There are two modes it can run:

- Batch Mode _(recommend)_:
  - Runs commands from a csv file
  - An example of csv file can be found in the `examples` dir
  - Variables:
    - csv:
- Single Mode
  - Variables:
    - `-p`, `--profile`, required=False,The name of the profile to be created
    - `-ip` `--ip`, required= False,The ip address of the profile
    - `-u`, `--username`, required=False,The username of the profile
    - `-pass`, `--password`, required= False,The password of the profile
    - `-i`, `--image`, required=False,A .tar file containing the Iox client software
    - `-a`, `--activation`, required=False,A json file containing the activation key
    - `-m`, `--mode`, required=False, choices=[`full`, `create`, `install`, `status`, `start`, `stop`, `uninstall`, `list`, `delete`], default=`full`, The mode of the program.
      - `full`: create profile, install, start the client. SSH to the AP and enable USB.
      - `create`: create profile.
      - `install`: install the client.
      - `start`: start the client.
      - `stop`: stop the client.
      - `status`: check the status of the client.
      - `uninstall`: uninstall the client.
      - `list`: list all the apps and states installed on the client.
      - `delete`: delete the profile
    - `-h`, `--help`, action=`help`, help=`show this help message and exit`

---
Author: Oliver Pan, 2022