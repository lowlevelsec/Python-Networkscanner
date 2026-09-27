import ipaddress


class Port:
	def __init__(self, number: int):
		self.number: int = number
		self.open: bool = False
		self.service: str | None = None
		self.protocol: str | None = None

	def __str__(self) -> str:
		status = "open" if self.open else "closed"
		service = self.service or "unknown"
		protocol = self.protocol or "unknown"

		return f"port {self.number}/{protocol}: {status} - {service}"


class Host:
	def __init__(self, ip: str):
		self.ip: str = ip
		self.ipv4: bool = ipaddress.ip_address(ip).version == 4
		self.ipv6: bool = ipaddress.ip_address(ip).version == 6
		self.mac: str | None = None
		self.arp: bool = False
		self.icmp: bool = False
		self.tcp: bool = False
		self.ports: list[Port] = []

	def __str__(self) -> str:
		methods = []

		if self.arp:
			methods.append("ARP")

		if self.icmp:
			methods.append("ICMP")

		if self.tcp:
			methods.append("TCP")

		discovery = ", ".join(methods) if methods else "none"

		return f"Host: {self.ip} - MAC: {self.mac or 'unknown'} - Discovery: {discovery}"
