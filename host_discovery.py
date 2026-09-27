# host discovery & network enumeration python
import ipaddress
from models import Host
from concurrent.futures import ThreadPoolExecutor
from scapy.all import (
	ARP,
	Ether,
	ICMP,
	IP,
	TCP,
	IPv6,
	ICMPv6EchoRequest,
	srp,
	sr1
)

# ARP subnet-scan
def arp_scan(subnet: str) -> list[tuple[str, str]]:
	network = ipaddress.ip_network(subnet, strict=False)

	# IPv4 check
	if network.version != 4:
		return []

	arp_request = ARP(pdst=subnet)
	ethernet_frame = Ether(dst="ff:ff:ff:ff:ff:ff")

	packet = ethernet_frame / arp_request
	answered, unanswered = srp(
		packet,
		timeout=2,
		verbose=False
	)

	hosts: list[tuple[str, str]] = []

	for sent, received in answered:
		hosts.append((received.psrc, received.hwsrc))

	return hosts

# IPv4 & IPv6 scapy ICPM-scan
def icmp_scan(ip_addr: str) -> bool:
	try:
		ip_version = ipaddress.ip_address(ip_addr).version

		# IPv4
		if ip_version == 4:
			packet = (
				IP(dst=ip_addr) /
				ICMP()
			)

		# IPv6
		if ip_version == 6:
			packet = (
				IPv6(dst=ip_addr) / ICMPv6EchoRequest()
			)

		response = sr1(
			packet,
			timeout=1,
			verbose=False
		)

		return response is not None

	except Exception:
		return False

# IPv4 & IPv6 TCP host scanning
def tcp_discovery(ip_addr: str) -> bool:

	target_ports = [
		21,	# ftp
		22,	# ssh
		23,	# telnet
		80,	# http
		443,	# https
		445,	# smb, kerberos
		3389	# rdp
	]

	ip_version = ipaddress.ip_address(ip_addr).version

	for port in target_ports:
		try:
			# IPv4
			if ip_version == 4:
				packet = (
					IP(dst=ip_addr) /
					TCP(dport=port,flags="S")
				)

			# IPv6
			elif ip_version == 6:
				packet = (
					IPv6(dst=ip_addr) /
					TCP(dport=port, flags="S")
				)

			else:
				return False

			response = sr1(
				packet,
				timeout=0.5,
				retry=0,
				verbose=False
			)

			if response is None:
				continue

			# SYN-ACK - port open
			if response.haslayer(TCP):
				flags = response[TCP].flags

				if flags & 0x12 == 0x12:
					return True

				# RST - port closed
				if flags & 0x04:
					True

		except Exception:
			continue

	return False

# subnet scan
def subnet_scan(
subnet: str,
arp: bool=True,
icmp: bool=True,
tcp: bool=True
) -> dict[str, Host]:
	network = ipaddress.ip_network(subnet, strict=False)

	network_clients: dict[str, Host] = {}

	# ARP-scanning
	if arp == True and network.version == 4:
		hosts: list[tuple[str, str]] = arp_scan(subnet)

		for ip_addr, mac_addr in hosts:

			if ip_addr not in network_clients:
				network_clients[ip_addr] = Host(
					ip_addr
				)

			client = network_clients[ip_addr]

			client.mac = mac_addr
			client.arp = True

	# ICMP scan - IPv4 & IPv6
	if icmp == True:
		with ThreadPoolExecutor(max_workers=100) as executor:

			results = executor.map(
				icmp_scan,
				(
					str(ip)
					for ip in network.hosts()
				)
			)

			for ip, alive in zip(
				network.hosts(),
				results
			):

				if not alive:
					continue

				ip_addr = str(ip)
				if ip_addr not in network_clients:
					network_clients[ip_addr] = Host(ip_addr)

				client = network_clients[ip_addr]
				client.icmp = True

	# common tcp-port host discovery
	if tcp == True:
		with ThreadPoolExecutor(max_workers=100) as executor:

			results = executor.map(
				tcp_discovery,
				(
					str(ip)
					for ip in network.hosts()
				)
			)

			for ip, alive in zip(
				network.hosts(),
				results
			):

				if not alive:
					continue

				ip_addr = str(ip)
				if ip_addr not in network_clients:
					network_clients[ip_addr] = Host(ip_addr)

				client = network_clients[ip_addr]
				client.tcp = True

	return network_clients
