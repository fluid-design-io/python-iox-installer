# Python IOx Installer

### install multiple iox_benja at once with python threading

# Introduction

This program is an automated installer for the Cisco Iox client software.
There are two modes it can run:

- Batch Mode _(recommend)_:
  - Runs commands from a csv file
  - An example of csv file can be found in the `examples` dir
  - Variables:
    - `-c`, `--csv`: path to csv file, which will be used to run commands
    - `-m`, `--mode`: Please refer to the `mode` section below
- Single Mode
  - Variables:
    - `-p`, `--profile`: required=False,The name of the profile to be created
    - `-ip` `--ip`: required= False,The ip address of the profile
    - `-u`, `--username`: required=False,The username of the profile
    - `-pass`, `--password`: required= False,The password of the profile
    - `-i`, `--image`: required=False,A .tar file containing the Iox client software
    - `-a`, `--activation`: required=False,A json file containing the activation key
    - `-m`, `--mode`: required=False, choices=[`full`, `create`, `install`, `status`, `start`, `stop`, `uninstall`, `list`, `delete`], default=`full`, The mode of the program.
      - `full`: `Default`, create profile, install, start the client.
      - `create`: create profile.
      - `delete`: delete the profile
      - `install`: install the client.
      - `uninstall`: uninstall the client.
      - `start`: start the client.
      - `stop`: stop the client.
      - `status`: check the status of the client.
      - `list`: list all the apps and states installed on the client.
    - `-h`, `--help`: show this help message and exit

---

# Example Commands

    #### Batch Mode
    **Full install**
    python3 iox_benja.py -c ./examples/example.csv
    **Create profile**
    python3 iox_benja.py -m create -c ./examples/example.csv
    **Delete profile**
    python3 iox_benja.py -m delete -c ./examples/example.csv
    **Install client**
    python3 iox_benja.py -m install -c ./examples/example.csv
    **Uninstall client**
    python3 iox_benja.py -m uninstall -c ./examples/example.csv
    **Start client**
    python3 iox_benja.py -m start -c ./examples/example.csv
    **Stop client**
    python3 iox_benja.py -m stop -c ./examples/example.csv
    **Status client**
    python3 iox_benja.py -m status -c ./examples/example.csv
    **List apps**
    python3 iox_benja.py -m list -c ./examples/example.csv




Author: Oliver Pan, 2022
