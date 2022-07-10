import json

def get_error_msg():
    with open('error.json') as f:
        error_msg = json.load(f)
    return error_msg
