# Generate .ini using variable server_ip
# Structure of .ini file:
# [benja_config]
# serial_dev: /dev/ttyUSB0
# server_ip: 192.168.100.30
# server_port1: 9302
# server_port2: 9303
# mode: TDOA
# debug: 0

import os
def getPath():
    path = ""
    if os.name == 'nt':
        path = ".\\"
    else:
        path = "./"
    return path

def gen_ini(ap_ip, server_ip):
    with open(f"{getPath()}package_config_{ap_ip}_{server_ip}.ini", "w") as f:
        f.write("[benja_config]\n")
        f.write("serial_dev: /dev/ttyUSB0\n")
        f.write("server_ip: " + server_ip + "\n")
        f.write("server_port1: 9302\n")
        f.write("server_port2: 9303\n")
        f.write("mode: TDOA\n")
        f.write("debug: 0\n")
    # return the name of the file
    return f.name

# delete .ini file


def del_ini(ap_ip, server_ip):
    os.remove(f"{getPath()}package_config_{ap_ip}_{server_ip}.ini")
