# Python Network Scanner

A lightweight and multithreaded network scanner written in Python for **TCP/UDP port scanning** and **IPv4 subnet host discovery** using ARP, ICMP, and TCP.

The scanner supports **IPv4 and IPv6**, configurable threading, common-service detection, HTTP/HTTPS server and version identification, customizable User-Agent spoofing, timing profiles, and MAC-address/vendor identification.

## Features

### Port Scanning

* TCP port scanning
* UDP port scanning
* IPv4 support
* IPv6 support
* Single-port selection
* Multiple-port selection
* Port-range selection
* Combination of ports and ranges
* Configurable thread count
* Port-based common-service detection
* HTTP/HTTPS `Server` header detection
* HTTP/HTTPS server and version identification
* Random or custom User-Agent spoofing
* Support for common:

  * Network services
  * Web services
  * Database services
  * Remote-access services
  * VPN services
  * Proxy services
  * Mail services
  * And more
* Timing templates with configurable:

  * Threads
  * Timeout
  * Delay

### Host Discovery / Subnet Scanning

* IPv4 subnet scanning
* ARP discovery
* ICMP discovery
* TCP SYN discovery
* Combination of multiple discovery methods
* Host deduplication across discovery methods
* MAC-address detection through ARP
* MAC-vendor identification through OUI lookup
* Multithreaded host discovery

Each discovered host is represented internally as a `Host` object. The object stores which discovery methods detected the host.

Example:

```text
Host: 192.168.178.1
MAC: b4:fc:51:74:e6:3d
Discovery: ARP, ICMP, TCP
```

---

# Requirements

* Python 3
* `requests`
* `scapy`

Install the required Python packages:

```bash
pip install requests scapy
```

Root privileges may be required for packet-based host discovery such as ARP, ICMP, and TCP SYN scanning:

```bash
sudo python3 portscanner.py ...
```

---

# Usage

## IPv4

Scan an IPv4 target:

```bash
python3 portscanner.py --ipv4 192.168.1.10
```

## IPv6

Scan an IPv6 target:

```bash
python3 portscanner.py --ipv6 2001:db8::1
```

---

# Port Selection

The scanner supports individual ports, multiple ports, and port ranges.

### Single port

```bash
python3 portscanner.py --ipv4 192.168.1.10 --ports 80
```

### Multiple ports

```bash
python3 portscanner.py --ipv4 192.168.1.10 -p 22,80,443
```

### Port range

```bash
python3 portscanner.py --ipv4 192.168.1.10 --ports 1-1024
```

### Combined ports and ranges

```bash
python3 portscanner.py --ipv4 192.168.1.10 -p 22,80,443,8000-8100
```

---

# Thread Count

The default number of threads is **100**.

Change the number of concurrent threads with `-t` or `--threads`:

```bash
python3 portscanner.py --ipv4 192.168.1.10 --threads 50
```

or:

```bash
python3 portscanner.py --ipv4 192.168.1.10 -t 50
```

The thread count can be used for both port scanning and subnet host discovery.

---

# Subnet / Host Discovery

Subnet scanning was introduced in **Version 1.3**.

Scan an IPv4 subnet:

```bash
sudo python3 portscanner.py --subnet 192.168.178.0/24
```

If no discovery method is explicitly selected, the scanner uses:

```text
ARP + ICMP + TCP
```

## ARP Discovery

```bash
sudo python3 portscanner.py --subnet 192.168.178.0/24 --arp
```

ARP discovery is intended for IPv4 hosts on the local Layer-2 network.

It can also retrieve the host's MAC address and identify the associated vendor when an OUI match is available.

## ICMP Discovery

```bash
sudo python3 portscanner.py --subnet 192.168.178.0/24 --icmp
```

ICMP discovery sends ICMP echo requests to determine whether hosts respond.

## TCP Discovery

```bash
sudo python3 portscanner.py --subnet 192.168.178.0/24 --tcp
```

TCP discovery sends SYN probes to a predefined set of commonly used TCP ports.

Currently checked ports include:

| Port | Service |
| ---: | ------- |
|   21 | FTP     |
|   22 | SSH     |
|   23 | Telnet  |
|   80 | HTTP    |
|  443 | HTTPS   |
|  445 | SMB     |
| 3389 | RDP     |

A TCP `SYN-ACK` or `RST` response is treated as evidence that the host is reachable.

---

# Combining Discovery Methods

Multiple discovery methods can be combined.

For example:

```bash
sudo python3 portscanner.py --subnet 192.168.178.0/24 --arp --icmp
```

or:

```bash
sudo python3 portscanner.py --subnet 192.168.178.0/24 --arp --icmp --tcp
```

When multiple discovery methods detect the same host, the scanner merges the results into a single `Host` object.

Example:

```text
Host: 192.168.178.1 - MAC: b4:fc:7d:00:ed:e8 - Discovery: ARP, ICMP, TCP
```

### Example Output

```text
scanning 192.168.178.0/24...

ARP: True
ICMP: True
TCP: True

found 13 host(s):

Host: 192.168.178.1 - MAC: b4:fc:7d:00:ed:e8 - Discovery: ARP, ICMP, TCP
Host: 192.168.178.22 - MAC: a8:48:fa:dd:bd:c4 - Discovery: ARP, ICMP
Host: 192.168.178.32 - MAC: ec:b5:fa:2c:e6:d5 - Discovery: ARP, ICMP, TCP
Host: 192.168.178.34 - MAC: unknown - Discovery: TCP
```

---

# Service Detection

The scanner contains a database of commonly associated ports and services.

Examples:

```text
22     → SSH
53     → DNS
80     → HTTP
443    → HTTPS
3306   → MySQL
5432   → PostgreSQL
3389   → RDP
```

Port-based service detection is based on commonly used port assignments. It does **not** guarantee that the expected service is actually running on that port.

For HTTP/HTTPS services, the scanner can additionally retrieve the HTTP `Server` response header to identify server software and version information when available.

HTTP version detection is only performed when:

```text
-v / --version
```

is enabled.

This prevents unnecessary HTTP requests when version detection is not requested.

---

# User-Agent Spoofing

The scanner supports both custom and randomly generated User-Agent strings.

### Custom User-Agent

```bash
python3 portscanner.py --ipv4 192.168.1.10 -u "Mozilla/5.0"
```

### Random User-Agent

```bash
python3 portscanner.py --ipv4 192.168.1.10 -r
```

or:

```bash
python3 portscanner.py --ipv4 192.168.1.10 --rand-uagent
```

---

# Scan Modes

## TCP-only Scanning

```bash
python3 portscanner.py --ipv4 192.168.1.10 -sT
```

or:

```bash
python3 portscanner.py --ipv4 192.168.1.10 --tcp-proxy
```

TCP connect scanning can be used with tools such as **ProxyChains**, where raw packet-based scanning is not suitable.

## UDP-only Scanning

```bash
python3 portscanner.py --ipv4 192.168.1.10 --udp
```

---

# Timing Templates

The scanner provides predefined timing profiles from `T0` to `T5`.

```bash
-T 0
-T 1
-T 2
-T 3
-T 4
-T 5
```

Timing profiles control scan parameters such as:

* Connection timeout
* Packet timeout
* Delay
* Scan speed

Higher timing levels use more aggressive timing parameters and can increase scan speed.

`T3` is the default timing profile.

---

# ARP / MAC Vendor Detection

With ARP discovery enabled, the scanner can retrieve the MAC address of discovered IPv4 hosts.

Example:

```text
Host: 192.168.178.1
MAC: b4:fc:7d:00:ed:e8
Vendor: AVM GmbH
Discovery: ARP, ICMP, TCP
```

Vendor identification is based on the MAC-address OUI when a matching vendor is available.

Locally randomized or unknown MAC addresses may be displayed as:

```text
Vendor: unknown
```

---

# HTTPS / TLS Services

The HTTP/HTTPS detection logic also recognizes services commonly associated with TLS.

The current HTTPS filter includes:

```text
https
smtps
imaps
pop3s
ldaps
mqtt-tls
amqp-tls
```

These services are treated as TLS-based services when determining whether HTTP-style version detection should be attempted.

---

# Project Structure

```text
Python-Networkscanner/
├── portscanner.py
├── host_discovery.py
├── models.py
├── http_header.py
└── services.py
```

## `portscanner.py`

Main scanner implementation.

Handles:

* TCP scanning
* UDP scanning
* IPv4/IPv6 socket handling
* Multithreading
* Port parsing
* Command-line argument parsing
* Timing profiles
* Subnet-scan integration

## `host_discovery.py`

Contains host-discovery functionality:

* ARP scanning
* ICMP scanning
* TCP SYN discovery
* IPv4 subnet enumeration
* Multithreaded host discovery
* MAC-address detection
* Vendor identification

## `models.py`

Contains the main data models used by the scanner:

* `Port`
* `Host`

The `Host` object stores information such as:

* IP address
* IP version
* MAC address
* MAC vendor
* ARP discovery status
* ICMP discovery status
* TCP discovery status
* Discovered ports

## `http_header.py`

Handles HTTP/HTTPS requests and extracts the HTTP `Server` response header for basic server and version identification.

The module uses the `HttpHeader` object to handle HTTP traffic.

## `services.py`

Contains the database of commonly associated network services and ports.

Examples:

```text
Port: 21  → Protocol: FTP
Port: 22  → Protocol: SSH
Port: 23  → Protocol: Telnet
Port: 25  → Protocol: SMTP
```

---

# Version History

## Version 2.0

### New Features

* Random and custom User-Agent spoofing
* HTTP/HTTPS `Server` header and version detection
* Optional HTTP version detection using `-v / --version`
* Configurable subnet-scanning threads
* TCP-only scanning with `-sT / --tcp-proxy`
* UDP-only scanning with `--udp`
* Timing templates from `T0` to `T5`
* MAC-address detection through ARP
* MAC-vendor identification through OUI lookup
* Improved subnet host discovery

## Version 1.3

### New Features

* IPv4 subnet scanning
* Host discovery
* ARP discovery
* ICMP discovery
* TCP discovery
* Combined ARP/ICMP/TCP discovery
* Host deduplication
* MAC-address detection through ARP
* `Host` objects for storing discovery information
* Single-port selection
* Multiple-port selection
* Port-range selection

## Version 1.2

### New Features

* HTTP/HTTPS header-based service and version detection
* Configurable thread count
* Expanded common-service database
* IPv6 support
* HTTPS support

---

# Disclaimer

This tool is intended for **authorized security testing, network administration, and educational purposes**.

Only scan systems and networks that you own or have explicit permission to test.

The author is not responsible for misuse of this software.
