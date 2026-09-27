python_portscanner

A lightweight network scanner written in Python for TCP and UDP port scanning and basic host discovery.

The scanner supports IPv4 and IPv6, configurable thread counts, common service detection, HTTP/HTTPS server identification, and subnet host discovery using ARP, ICMP, and TCP.

Features
Port Scanning
TCP port scanning
UDP port scanning
IPv4 support
IPv6 support
Single port selection
Port range selection
Multiple port selection
Configurable number of threads
Port-based common service detection
HTTP/HTTPS service detection
HTTP Server header detection
Basic server software/version identification
Support for common network, database, remote-access, VPN, proxy, and other services
Host Discovery / Subnet Scanning

The scanner can discover active hosts in a subnet using multiple discovery methods:

ARP discovery
ICMP discovery
TCP discovery
IPv4 subnet scanning
Combination of multiple discovery methods
Host deduplication across discovery methods
MAC address detection through ARP

Each discovered host is represented internally as a Host object and records which discovery methods detected it.

Example:

Host: 192.168.178.1 - MAC: b4:fc:7d:00:ed:e8 - Discovery: ARP, ICMP, TCP
Requirements
Python 3
requests
scapy

Install the required Python packages with:

pip install requests scapy

Root privileges may be required for ARP, ICMP, and TCP packet-based host discovery:

sudo python3 portscanner.py ...
Usage
IPv4

Scan an IPv4 target:

python3 portscanner.py --ipv4 192.168.1.10
IPv6

Scan an IPv6 target:

python3 portscanner.py --ipv6 2001:db8::1
Port Selection

The scanner supports individual ports, multiple ports, and port ranges.

Single port:

python3 portscanner.py --ipv4 192.168.1.10 --ports 80

Multiple ports:

python3 portscanner.py --ipv4 192.168.1.10 --ports 22,80,443

Port range:

python3 portscanner.py --ipv4 192.168.1.10 --ports 1-1024

Multiple ports and ranges can also be combined:

python3 portscanner.py --ipv4 192.168.1.10 --ports 22,80,443,8000-8100
Thread Count

The default number of threads is 100.

Change the number of threads with -t or --threads:

python3 portscanner.py --ipv4 192.168.1.10 --threads 50

or:

python3 portscanner.py --ipv4 192.168.1.10 -t 50
Subnet / Host Discovery

Version 1.3 introduces subnet scanning and host discovery.

Scan a subnet:

sudo python3 portscanner.py --subnet 192.168.178.0/24

When no discovery method is specified, the scanner uses:

ARP
ICMP
TCP
ARP Discovery
sudo python3 portscanner.py --subnet 192.168.178.0/24 --arp

ARP discovery is used for IPv4 hosts on the local network and can also provide the host's MAC address.

ICMP Discovery
sudo python3 portscanner.py --subnet 192.168.178.0/24 --icmp

ICMP discovery checks whether hosts respond to ICMP echo requests.

TCP Discovery
sudo python3 portscanner.py --subnet 192.168.178.0/24 --tcp

TCP discovery sends SYN probes to a predefined set of commonly used TCP ports.

Currently checked ports include:

21    FTP
22    SSH
23    Telnet
80    HTTP
443   HTTPS
445   SMB
3389  RDP

A SYN-ACK or TCP RST response is treated as evidence that the host is reachable.

Combining Discovery Methods

Discovery methods can be combined:

sudo python3 portscanner.py --subnet 192.168.178.0/24 --arp --icmp

or:

sudo python3 portscanner.py --subnet 192.168.178.0/24 --arp --icmp --tcp

Hosts discovered by multiple methods are merged into a single host entry.

Example:

Host: 192.168.178.1 - MAC: b4:fc:7d:00:ed:e8 - Discovery: ARP, ICMP, TCP
Example Output
scanning 192.168.178.0/24...

ARP: True
ICMP: True
TCP: True

found 13 host(s):

Host: 192.168.178.1 - MAC: b4:fc:7d:00:ed:e8 - Discovery: ARP, ICMP, TCP
Host: 192.168.178.22 - MAC: a8:48:fa:dd:bd:c4 - Discovery: ARP, ICMP
Host: 192.168.178.32 - MAC: ec:b5:fa:2c:e6:d5 - Discovery: ARP, ICMP, TCP
Service Detection

The scanner contains a database of commonly used ports and their associated services.

For example:

22     → ssh
53     → dns
80     → http
443    → https
3306   → mysql
5432   → postgresql
3389   → rdp

These mappings represent commonly associated services and do not guarantee that a particular service is actually running on a port.

For HTTP/HTTPS services, the scanner additionally attempts to retrieve the HTTP Server response header to identify server software and version information when available.

Version 1.3

New features:

Subnet scanning
Host discovery
ARP discovery
ICMP discovery
TCP discovery
Combined ARP/ICMP/TCP discovery
MAC address detection through ARP
Host objects for storing discovery information
Single port selection
Port range selection
Multiple port selection
Version 1.2

New features:

HTTP/HTTPS header-based service and version detection
Configurable thread count
Expanded common-service database
IPv6 support
HTTPS support
Project Structure
python_portscanner/
├── portscanner.py
├── host_discovery.py
├── models.py
├── http_header.py
└── services.py
portscanner.py

Main scanner implementation including:

TCP scanning
UDP scanning
IPv4/IPv6 socket handling
Multithreading
Port parsing
Command-line argument parsing
Subnet scan integration
host_discovery.py

Contains the host discovery functionality:

ARP scanning
ICMP scanning
TCP discovery
Subnet enumeration
Multithreaded host discovery
models.py

Contains the data models used by the scanner:

Port
Host

The Host object stores information such as:

IP address
IPv4/IPv6
MAC address
ARP discovery status
ICMP discovery status
TCP discovery status
Discovered ports
http_header.py

Handles HTTP/HTTPS requests and extracts the Server response header for basic server and version identification.

services.py

Contains the database of commonly associated network services and ports.

Disclaimer

Only scan systems and networks that you own or have explicit permission to test.

The author is not responsible for misuse of this software.
