from netmiko import ConnectHandler

from util import debug_print


def ssh_add_usb_module(ap_ip, ap_username, ap_password, ap_secret, debug_enabled=False):
    device = {'device_type': 'cisco_ios',
              'ip': ap_ip,
              'username': ap_username,
              'password': ap_password,
              'secret': ap_secret,
              }
    conn = ConnectHandler(**device)
    if not conn.check_enable_mode():
        conn.enable()
    output = conn.send_command('test usb load module ftdi-sio vendor-id 403 product-id 6015 version 1000')
    conn.send_command('test usb disable')
    conn.send_command('test usb enable')
    # This allows the AP to turn on USB and load the module
    debug_print(output, debug_enabled)
    conn.send_command('end')
    conn.read_channel()
    conn.disconnect()
    return output
