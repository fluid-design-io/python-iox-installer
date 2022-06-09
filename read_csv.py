import os
import pandas as pd
from util import get_cwd

# This function will store the variables from the excel file.
def read_csv(file_path):
    cwd = get_cwd(file_path)
    print(cwd)
    df = pd.read_csv(cwd)
    print("\n")
    return df
