# python portscanner
import socket
import argparse
from models import Port
from services import common_services
from http_header import request_header
from host_discovery import subnet_scan
from concurrent.futures import ThreadPoolExecutor
socket.setdefaulttimeout(0.5)
parser = argparse.ArgumentParser(description="TCP/UDP - portscanner")
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("--ipv4", type=str, help="target IPv4 address")
group.add_argument("--ipv6", type=str, help="target IPv6 address" )
group.add_argument("-sn", "--subnet", type=str, help="subnet to scan")
parser.add_argument("-t", "--threads", type=int, help="number of threads", default=100)
parser.add_argument("-p", "--ports", type=str, help="port range (-p 1-1000, 22,443,445)")
parser.add_argument("--arp", action="store_true", help="ARP host discovery")
parser.add_argument("--icmp", action="store_true", help="ICMP host discovery")
parser.add_argument("--tcp", action="store_true", help="TCP host discovery")

args = parser.parse_args()

# tcp/IPV4 portscanning
def tcp_scan(scan_ip: str, scan_port: int, ipv6: bool = False) -> Port | None:
	internet_protocol = socket.AF_INET6 if ipv6 else socket.AF_INET
	tcp_socket = socket.socket(internet_protocol, socket.SOCK_STREAM)

	# tcp scan
	result = tcp_socket.connect_ex((scan_ip, scan_port))
	tcp_socket.close()

	if result == 0:
		tcp_port = Port(int(scan_port))
		tcp_port.open = True
		tcp_port.protocol = "TCP"

		# service detection
		if tcp_port.number in common_services:
			tcp_port.service = common_services[scan_port]

		return tcp_port

# udp/IPV4 portscanning
def udp_scan(scan_ip: str, scan_port: int, ipv6: bool = False) -> Port | None:

	# udp scan
	internet_protocol = socket.AF_INET6 if ipv6 else socket.AF_INET
	with socket.socket(internet_protocol, socket.SOCK_DGRAM) as udp_socket:

		try:
			udp_socket.sendto(b'str', (scan_ip, scan_port))
			udp_response = udp_socket.recvfrom(1024)

		except socket.timeout:
			return None

	udp_port = Port(int(scan_port))
	udp_port.open = True
	udp_port.protocol = "UDP"
	udp_port.service = common_services.get(scan_port)

	return udp_port

def parse_ports(port_string: str) -> list[int]:
	ports: list[int] = []

	for part in port_string.split(","):

		if "-" in part:
			start, end = part.split("-")
			ports.extend(range(int(start), int(end) + 1))
		else:
			ports.append(int(part))

	return ports

# main portscan + http-header service & version detection
def portscanning(target: str, port: int, ipv6: bool = False) -> list[Port]:
	results: list[Port] = []

	tcp_result = tcp_scan(target, port, ipv6)

	if tcp_result:
		http_header = request_header(
			ip_addr=target,
			port=port,
			common_service=tcp_result.service,
			ipv6=ipv6
		)

		if http_header:
			results.append(http_header)

		else:
			results.append(tcp_result)

	udp_result = udp_scan(target, port, ipv6)

	if udp_result:
		results.append(udp_result)

	return results

def main(target: str, ipv6: bool = False) -> list[Port]:

	if args.ports:
		ports: list[int] = parse_ports(args.ports)

	else:
		ports: list[int] = list(range(1, 10001))

	scanned_ports: list[Port] = []

	# multi threading
	with ThreadPoolExecutor(max_workers=args.threads) as executor:

		results = executor.map(
			lambda scan_port: portscanning(target, port, ipv6),
			ports
		)

		for result in results:
			scanned_ports.extend(result)

	return scanned_ports

def subnet_main(subnet: str) -> None:

	scan_arp = args.arp
	scan_icmp = args.icmp
	scan_tcp = args.tcp

	protocols = (scan_arp, scan_icmp, scan_tcp)

	if not any(protocols):
		scan_arp = True
		scan_icmp = True
		scan_tcp = True

	print(f"scanning {subnet}...")
	print(
		f"\nARP: {scan_arp}"
		f"\nICMP: {scan_icmp}"
		f"\nTCP: {scan_tcp}"
	)

	hosts = subnet_scan(subnet=subnet, arp=scan_arp, icmp=scan_icmp, tcp=scan_tcp)

	if not hosts:
		print("no active hosts found")
		return

	print(f"found {len(hosts)} host(s):")
	print()

	for ip_addr, host in hosts.items():
		print(host)

if __name__ == "__main__":

	if args.threads < 1:
		parser.error("minimum Thread amount: 1")

	if args.subnet:
		subnet_main(args.subnet)

	elif args.ipv6:
		target_ip: str = args.ipv6
		ipv6: bool = True

		print(f"scanning {target_ip}...")
		results = main(target=target_ip, ipv6=ipv6)

		for scanned_ports in results:
			print(scanned_ports)

	elif args.ipv4:
		target_ip: str = args.ipv4
		ipv6: bool = False

		print(f"scanning {target_ip}...")
		results = main(target=target_ip, ipv6=ipv6)

		for scanned_port in results:
			print(scanned_port)

