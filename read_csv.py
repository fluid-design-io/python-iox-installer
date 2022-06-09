import os
import pandas as pd

# Variables in csv file:
#  - ap_profile: the name of the profile to be created
#  - ap_ip: the ip address of the profile
#  - ap_username: the username of the profile
#  - ap_password: the password of the profile
#  - ap_image_path: a .tar file containing the Iox client software
#  - ap_activation: a json file containing the activation key
# The program reads these variables from an excel or csv file.

# A function to get current working directory.


def get_cwd():
    cwd = os.getcwd()
    return cwd

# This function will store the variables from the excel file.


def read_csv(file_path):
    cwd = get_cwd()
    print("Reading csv file...")
    df = pd.read_csv(cwd + "/" + file_path)
    print("csv file read")
    print("\n")
    return df
