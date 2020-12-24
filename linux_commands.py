import subprocess


class LinuxCommands:
    def __init__(self):
        self.interfaces = subprocess.run("ifconfig -s | awk '{print $1}'| awk 'FNR>1'", shell=True, capture_output=True)
        self.interfaces_list = self.interfaces.stdout.decode().split('\n')[0:-1]

    @staticmethod
    def print_ip() -> None:
        ip = subprocess.run(['wget', '-qO-', 'eth0.me'], capture_output=True)
        print(ip.stdout.decode())

    def print_mac_address(self) -> None:
        int_list = list(self.interfaces_list)
        int_list.remove("lo")
        mac = subprocess.run("ifconfig -a | grep ether | awk '{print $2}'", shell=True, capture_output=True)
        mac = mac.stdout.decode().split('\n')[0:-1]

        for i in range(len(mac)):
            print("MAC Address: " + str(mac[i]) + " of the interface " + str(int_list[i]))

    def print_netmask(self) -> None:
        for interface in self.interfaces_list:
            mask = subprocess.run("ifconfig " + str(interface) + " | grep netmask | awk '{print $4}'", shell=True,
                                  capture_output=True)
            mask = mask.stdout.decode().split('\n')
            if mask[0] != '':
                print(str(interface) + " has netmask " + mask[0])

    def print_available_ap(self) -> None:
        ap_info = dict()

        for iface_name in self.interfaces_list:
            full_iface_name = subprocess.run("ifconfig | grep " + str(iface_name) + " | awk '{print $1}'", shell=True,
                                             capture_output=True)
            full_iface_name = full_iface_name.stdout.decode().split('\n')[0][0:-1]
            info = subprocess.run("iwconfig " + full_iface_name + " | grep 'Access Point' ", shell=True,
                                  capture_output=True)

            info = info.stdout.decode().split('\n')[0]
            if 'Access Point' in info:
                ap_info[iface_name] = "AP"
            else:
                ap_info[iface_name] = "NO AP"

        return ap_info


if __name__ == "__main__":
    command = LinuxCommands()
    print("IP: ")
    command.print_ip()
    command.print_mac_address()
    print("Netmasks: ")
    command.print_netmask()
    print("AP: ")
    print(command.print_available_ap())

