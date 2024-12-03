# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 11:56:39 2024

@author: GODWIN
"""

# Router names
router = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.1',  # Replace with router's IP
    'username': 'admin',     # Replace with your SSH username
    'password': 'password',  # Replace with your SSH password
}

# Configuration commands
commands = [
    'interface Loopback0',
    'ip address 192.168.1.1 255.255.255.0',
    'no shutdown',
    'interface GigabitEthernet0/0',
    'ip address 192.168.10.1 255.255.255.0',
    'no shutdown',
    'router ospf 1',
    'network 192.168.1.0 0.0.0.255 area 0',
    'network 192.168.10.0 0.0.0.255 area 0',
]

try:
    # Connect to the router
    print("Connecting to the router...")
    net_connect = ConnectHandler(**router)
    print("Connected!")

    # Apply the configuration
    print("Configuring the router...")
    net_connect.send_config_set(commands)
    net_connect.send_command('write memory')
    print("Configuration applied and saved.")

    # Confirm configuration
    ospf_output = net_connect.send_command("show ip ospf neighbor")
    route_output = net_connect.send_command("show ip route")

    print("\nOSPF Neighbors:\n", ospf_output)
    print("\nRouting Table:\n", route_output)

    # Disconnect
    net_connect.disconnect()
    print("Disconnected from the router.")

except Exception as error:
    print(f"An error occurred: {error}")
