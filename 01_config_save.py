import os
import yaml
from netmiko import ConnectHandler


def find_lab_file():
    clab_file = [i for i in os.listdir() if i.endswith("yaml")]
    if clab_file:
        return clab_file[0]
    else:
        return None


lab_file = find_lab_file()
if lab_file:
    clab_yaml = yaml.safe_load(open(lab_file))
else:
    print("=> Could not find clab file...")


for host, host_data in clab_yaml["topology"]["nodes"].items():
    file_name = f"{host}.cfg"
    if "CE" in host:
        username, password = "admin", "admin"
        device_type = "cisco_ios"
    else:
        username, password = "clab", "clab@123"
        device_type = "cisco_xr"
    device_object = {
        "host": host_data["mgmt-ipv4"],
        "device_type": device_type,
        "username": username,
        "password": password,
    }
    with ConnectHandler(**device_object) as conn:
        output = conn.send_command("show running-config")
        with open(file_name, "w+") as config_file:
            config_file.write(output)
