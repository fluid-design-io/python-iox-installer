import pandas as pd

# This function will store the variables from the excel file.
def read_csv(file_path):
    df = pd.read_csv(file_path)
    print("\n")
    return df
