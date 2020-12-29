import subprocess


class LinuxCommands:
    def __init__(self):
        self.interfaces = subprocess.run("ifconfig -s | awk '{print $1}'| "
                                         "awk 'FNR>1'",
                                         shell=True, capture_output=True)
        self.interfaces_list = self.interfaces.stdout.decode()
        self.interfaces_list = self.interfaces_list.split('\n')[0:-1]

    @staticmethod
    def print_ip() -> None:
        ip = subprocess.run(['wget', '-qO-', 'eth0.me'], capture_output=True)
        print(ip.stdout.decode())

    def print_mac_address(self) -> dict:
        int_list = list(self.interfaces_list)
        int_list.remove("lo")
        mac = subprocess.run("ifconfig -a | grep ether | awk '{print $2}'",
                             shell=True, capture_output=True)
        mac = mac.stdout.decode().split('\n')[0:-1]
        mac_dict = dict()
        for i in range(len(mac)):
            mac_dict[str(int_list[i])] = str(mac[i])
        return mac_dict

    def print_netmask(self) -> dict:
        mask_dict = dict()
        for interface in self.interfaces_list:
            mask = subprocess.run("ifconfig " + str(interface) +
                                  " | grep netmask | awk '{print $4}'",
                                  shell=True,
                                  capture_output=True)
            mask = mask.stdout.decode().split('\n')
            if mask[0] != '':
                mask_dict[str(interface)] = mask[0]
        return mask_dict

    def print_available_ap(self) -> dict:
        ap_info = dict()

        for iface_name in self.interfaces_list:
            full_iface_name = subprocess.run("ifconfig | grep " +
                                             str(iface_name) +
                                             " | awk '{print $1}'",
                                             shell=True,
                                             capture_output=True)
            full_iface_name = full_iface_name.stdout.decode()
            full_iface_name = full_iface_name.split('\n')[0][0:-1]
            info = subprocess.run("iwconfig " + full_iface_name +
                                  " | grep 'Access Point' ", shell=True,
                                  capture_output=True)

            info = info.stdout.decode().split('\n')[0]
            if 'Access Point' in info:
                ap_info[iface_name] = "AP"
            else:
                ap_info[iface_name] = "NO AP"

        return ap_info


if __name__ == "__main__":
    command = LinuxCommands()
    print("External IP: ")
    command.print_ip()
    mac_addresses = command.print_mac_address()
    netmasks = command.print_netmask()
    ap = command.print_available_ap()

    for iface in ap.keys():
        print("--------------------")
        print(iface)
        if iface in mac_addresses:
            print("MAC-ADDRESS: " + str(mac_addresses[iface]))
        if iface in netmasks:
            print("NETMASK: " + str(netmasks[iface]))
        if iface in ap:
            print(str(ap[iface]))
        print("--------------------")

