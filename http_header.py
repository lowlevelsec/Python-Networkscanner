# http-header service & version detection python
import requests
from models import Port
from user_agents import user_agent_dict

# create header object
class HttpHeader(Port):

	def __init__(self, number: int):

		super().__init__(number)
		self.version: str | None = None

	def __str__(self):
		status = "open" if self.open else "closed"
		service = self.service or "unknown"
		version = self.version or "unknown"

		return f"port {self.number}/TCP: {status} - {service} {version}"

# request http-headers
def request_header(ip_addr: str, port: int, common_service: str | None,
ipv6: bool = False, user_agent: str | None = None) -> HttpHeader | None:
	try:

		tls_services = (
			"https",
			"smtps",
			"imaps",
			"pop3s",
			"ldaps",
			"mqtt-tls",
			"amqp-tls"
		)

		if common_service in tls_services:
			http_protocol = "https"

		else:
			http_protocol = "http"

		target_url = f"{http_protocol}://{ip_addr}:{port}/"

		if ipv6 == True:
			target_url = f"{http_protocol}://[{ip_addr}]:{port}/"

		headers = {}

		if user_agent == True:
			headers["User-Agent"] = user_agent

		response = requests.get(
			target_url,
			headers=headers,
			timeout=1
		)

		server_header = HttpHeader(port)

		server_header.open = True
		server_header.service = common_service
		server_header.version = response.headers.get("Server")

		return server_header

	except requests.RequestException:
		return None
