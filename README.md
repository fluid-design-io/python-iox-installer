# Python IOx Installer

### install multiple iox_benja at once 🕛

# Introduction

This program is an automated installer for the Cisco Iox client software.

# Features

- Import a list of Iox devices from a CSV file
- Create/delete multiple iox profiles
- Install multiple Iox clients
- Generate package_config.ini file automatically based on profile ip
- Check AP status and list of installed apps
- Threading support, runs multiple ioxclient at once
- Simplified listing status, list and profiles overhead, only showing what's important

# Requirements

    # Reqires Python 3.6+
    pip install -r requirements.txt

Download ioxclient from [here](https://developer.cisco.com/docs/iox/#!iox-resource-downloads)
Then unzip the file and move it to the same directory as this program, make sure the 'ioxclient' is inside the directory

Make sure you have the `package_benja.tar` file in the same directory as this program.

# Usage

    python iox_benja.py # variables...

    # Run the program with the --help flag to see the usage

# Issues

Currently you have to manually go through the day0 configuration when ioxclient is installed. Otherwise the program cannot create the profiles.

# Commands

There are two modes it can run:

- Batch Mode _(recommend)_:
  - Runs commands from a csv file
  - An example of csv file can be found in the `examples` dir
  - Variables:
    - `-c`, `--csv`: path to csv file, which will be used to run commands. Default is `iox_install.csv`
    - `-m`, `--mode`: Please refer to the `mode` section below. Default is `full`
- Single Mode
  - Variables:
    - `-p`, `--profile`: required=False,The name of the profile to be created
    - `-ip` `--ip`: required= False,The ip address of the profile
    - `-u`, `--username`: required=False,The username of the profile
    - `-pass`, `--password`: required= False,The password of the profile
    - `-s`, `--secret`: The enable secret of the profile
    - `-i`, `--image`: required=False,A .tar file containing the Iox client software
    - `-a`, `--activation`: required=False,A json file containing the activation key
    - `-s`, `--server`: required=False,The ip address of the server, used when generating package_config.ini
    - `-m`, `--mode`: required=False, choices=[`full`, `create`, `install`, `status`, `start`, `stop`, `uninstall`, `list`, `delete`, `profiles`], default=`full`, The mode of the program.
      - `full`: `Default`, create profile, install, start the client.
      - `create`: create profile.
      - `delete`: delete the profile
      - `install`: install the client.
      - `uninstall`: uninstall the client.
      - `start`: start the client.
      - `stop`: stop the client.
      - `status`: check the status of the client.
      - `list`: list all the apps and states installed on the client.
      - `profiles`: list all the profiles.
    - `-h`, `--help`: show this help message and exit

---

# Example Commands

**Full install**

    python iox_benja.py -c ./examples/iox_install.csv

**Create profile**

    python iox_benja.py -c ./examples/iox_install.csv -m create 

**Delete profile**

    python iox_benja.py -c ./examples/iox_install.csv -m delete 

**Install client**

    python iox_benja.py -c ./examples/iox_install.csv -m install 

**Uninstall client**

    python iox_benja.py -c ./examples/iox_install.csv -m uninstall 

**Start client**

    python iox_benja.py -c ./examples/iox_install.csv -m start 

**Stop client**

    python iox_benja.py -c ./examples/iox_install.csv -m stop 

**Status client**

    python iox_benja.py -c ./examples/iox_install.csv -m status 

**List apps**

    python iox_benja.py -c ./examples/iox_install.csv -m list 

**List profiles**

    python iox_benja.py -c ./examples/iox_install.csv -m profiles


https://user-images.githubusercontent.com/13263720/173143602-21cdb3c4-279f-4ecd-be3d-919834ae0fca.mp4


---

License: MIT
Author: Oliver Pan, 2022
