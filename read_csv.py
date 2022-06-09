import os
import pandas as pd

# A function to get current working directory.
def get_cwd():
    cwd = os.getcwd()
    return cwd

# This function will store the variables from the excel file.
def read_csv(file_path):
    cwd = get_cwd()
    df = pd.read_csv(cwd + "/" + file_path)
    print("\n")
    return df
