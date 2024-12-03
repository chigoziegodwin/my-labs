# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 18:53:48 2024

@author: GODWIN
"""

#assuming SSH or telnet access to the router via a script or automation tool like Ansible

#variables 
ROUTER_IP = "192.168.1.1"  # IP address of the router for SSH/Telnet
USERNAME = "admin"         # Username for the router
PASSWORD = "password"      #password for the router
LOOPBACK_IP = "10.0.0.1"   #Loopback IP address
PHYSICAL_IF = "GigabitEthernet0/0"
PHYSICAL_IP = "192.168.2.1" # IP address for the physical interface
OSPF_PROCESS_ID = "1"
NETWORKS = ("10.0.0.0 0.0.0.255" , "192.168.2.0 0.0.0.255") #Networks to promote

# Script commands
cat << EOF > configure_router.sh
#!/usr/bin/expect -f


# waits for 12 seconds for user input or reaction
set timeout 12

spawn ssh admin@192.168.1.1
expect "password" #expects a password prompt
send  "${PASSWORD}\r" #send the password
expect ">"
send "enable\r"
expect "password:"
send "${PASSWORD}\r"
expect "#"
send "configure terminal\r"

#configure loopback
send "interface loopback0\r"
send "ip address ${LOOPBACK_IP} 255.255.255.255\r"
send "no shutdown\r"

#configure physical interface
send "interface ${PHYSICAL_IF}\r"
send "ip address ${PHYSICAL_IP} 255.255.255.0\r"
send "no shutdown\r"

#configure OSPF
send "router ospf ${OSPF_PROCESS_ID}\r"
EOF

foreach net $NETWORKS {              
    append net_cmd "send \"network $net area 0\\r"\n"
}


cat << EOF >> configure_router.sh
${net_cmd}
send "end\r"
send "write memory\r"
expect "#"
send "exit\r"
EOF

chmod +x configure_router.sh
-/configure_router.sh




