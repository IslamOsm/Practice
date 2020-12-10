import os


class LinuxCommands:

    @staticmethod
    def print_ip() -> None:
        ip = os.popen('wget -qO- eth0.me').read()
        print(ip)

    @staticmethod
    def print_mac_address() -> None:
        mac = os.popen("ifconfig -a | grep ether | gawk '{print $2}'").readlines(0)
        print(mac[1])

    @staticmethod
    def print_netmask() -> None:
        masks = os.popen("ifconfig | grep netmask | gawk '{print $4}'").read()
        print(masks)

    @staticmethod
    def print_available_ap() -> None:
        interfaces = os.popen("ifconfig -s | awk '{print $1}'| awk 'FNR>1'").readlines(0)
        ap_info = dict()

        for iface_name in interfaces:
            info = os.popen("iwconfig " + iface_name[0:-1] + " | grep 'Access Point' ").read()

            if 'Access Point' in info:
                ap_info[iface_name[0:-1]] = "AP"
            else:
                ap_info[iface_name[0:-1]] = "NO AP"

        return ap_info


if __name__ == "__main__":
    print("AP: ")
    print(LinuxCommands.print_available_ap())
    print("IP: ")
    LinuxCommands.print_ip()
    print("MAC Address: ")
    LinuxCommands.print_mac_address()
    print("Netmasks: ")
    LinuxCommands.print_netmask()
