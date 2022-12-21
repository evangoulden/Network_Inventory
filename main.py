import napalm
import netmiko.exceptions
import paramiko.ssh_exception


def init():
    driver = napalm.get_network_driver("ios")
    with open("port_totals.csv", 'a') as port_totals:
        port_totals.write("Switch Name, Up Ports, Down Ports, Total Ports\n")

        with open("host_list.txt", 'r') as host_list:
            for host in host_list.readlines():
                device = driver(
                    hostname=f"{host}",
                    username="net-services",
                    password="ns0905",
                    optional_args={"port": 23},
                )
                try:
                    print(f"Opening {host}")
                    device.open()
                    name = device.get_facts()
                    with open(f"{name['hostname']}_interface_list.txt", 'w') as f:
                        port_count = 0
                        up_ports = 0
                        down_ports = 0
                        for key, value in device.get_interfaces().items():
                            if 'Giga' in key:
                                f.write(key + ": " + str(value) + "\n")
                                port_count = port_count + 1
                                if value["is_up"] is True:
                                    up_ports = up_ports + 1
                                else:
                                    down_ports = down_ports + 1
                            elif 'Fast' in key:
                                f.write(key + ": " + str(value) + "\n")
                                port_count = port_count + 1
                                if value["is_up"] is True:
                                    up_ports = up_ports + 1
                                else:
                                    down_ports = down_ports + 1
                            elif 'Eth' in key:
                                f.write(key + ": " + str(value) + "\n")
                                port_count = port_count + 1
                            else:
                                continue
                            f.write(f"Total ports: {port_count}\n")
                            f.write(f"Up ports: {up_ports}\n")
                            f.write(f"Down ports: {down_ports}\n")
                        port_totals.write(f"{name['hostname']}, {up_ports}, {down_ports}, {port_count}\n")
                    f.close()
                    device.close()
                    print(f"Device Closed... {host}")
                except netmiko.exceptions.ReadTimeout as Ex:
                    print(f"Exception Occurred {Ex} ")
                except napalm.base.exceptions.ConnectionException as Ex:
                    print(f"Exception Occurred {Ex} ")
                except netmiko.exceptions.NetmikoAuthenticationException as Ex:
                    print(f"Exception Occurred {Ex} ")
                except paramiko.ssh_exception.AuthenticationException as Ex:
                    print(f"Exception Occurred {Ex} ")

    f.close()
    port_totals.close()


if __name__ == '__main__':
    init()
