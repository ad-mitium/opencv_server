#!/usr/bin/env python3
# Authored by Timothy Mui 3/28/2023

import netifaces

host = {
    'host_port':5100 ,
    'host_ip': '0.0.0.0'    
}

ethernet_device = 1
iface = netifaces.interfaces()
host_ip = netifaces.ifaddresses(iface[ethernet_device])[2][0]['addr']     # This bit of code assumes you are using the first ethernet device to host

host_address = host_ip
# host_address = host['host_ip']
