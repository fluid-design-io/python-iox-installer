# Python IOx Installer

### install multiple iox_benja at once 🕛

# Introduction

This program is an automated installer for the Cisco Iox client software.

# Features

- 🗄 Import a list of Iox devices from a CSV file
- 👥 Create/delete multiple iox profiles
- 📦 Install multiple Iox clients
- 💡 SSH support for enable AP configurations
- 🔧 Generate package_config.ini file automatically based on profile ip
- ✅ Check AP status and list of installed apps
- 🏎 Threading support, runs multiple ioxclient at once
- 📄 Simplified listing status, list and profiles overhead, only showing what's important
- 🌎 Localization support, see [🌎 Localization](#localization)

# Requirements

    # Reqires Python 3.6+
    pip install -r requirements.txt

Download ioxclient from [here](https://developer.cisco.com/docs/iox/#!iox-resource-downloads)
Then unzip the file and move it to the same directory as this program, make sure the 'ioxclient' is inside the directory

Make sure you have the `package_benja.tar` file in the same directory as this program.

# Usage

    python iox_benja.py # variables...

    # Run the program with the --help flag to see the usage

Example usage: [here](#example-commands)

# Commands

There are two modes it can run:

- Batch Mode _(recommend)_:
  - Runs commands from a csv file
  - An example of csv file can be found in the `examples` dir
- Single Mode:
  - Runs a single command from the following actions

# Variables

| Argument | Value | Description | Required | Default | Type |
| -------- | ---- | ----------- | -------- | ------- | ---- |
| -c, --csv | csv_path | The csv file containing the variables. | No | iox_install.csv | str |
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

# Example Commands

**Full install**

    python iox_benja.py
    # Or install a particular csv file
    python iox_benja.py -c iox_install.csv

**Create profile**

    python iox_benja.py -m create 

**Delete profile**

    python iox_benja.py -m delete 

**Install client**

    python iox_benja.py -m install 

**Uninstall client**

    python iox_benja.py -m uninstall 

**Start client**

    python iox_benja.py -m start 

**Stop client**

    python iox_benja.py -m stop 

**Status client**

    python iox_benja.py -m status 

**List apps**

    python iox_benja.py -m list 

**List profiles**

    python iox_benja.py -m profiles

**Switch language**

    python iox_benja.py -l ko

**Enable debug mode**

    python iox_benja.py -d

**Check version**

    python iox_benja.py -v

# Localization

- English
- Korean

https://user-images.githubusercontent.com/13263720/173143602-21cdb3c4-279f-4ecd-be3d-919834ae0fca.mp4

# Contributing

- Fork the repository
- Create a new branch
- Add your changes
- Commit your changes
- Push your changes to the remote repository
- Open an issue or pull request
- Keep in touch

---

# License

MIT License
Author: Oliver Pan, 2022
