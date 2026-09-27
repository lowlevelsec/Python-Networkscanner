mac_vendors = {
	"00:00:5E": "IANA",
	"00:00:0C": "Cisco Systems",
	"00:0C:29": "VMware",
	"00:1C:42": "Parallels",
	"00:1B:21": "Intel Corporate",
	"00:1B:63": "Apple",
	"00:25:90": "Hewlett-Packard",
	"00:24:E4": "Dell",
	"3C:5A:37": "Apple",
	"3C:22:FB": "Apple",

	"B8:27:EB": "Raspberry Pi",
	"DC:A6:32": "Raspberry Pi",

	"F0:D5:BF": "AVM",
	"34:81:C4": "AVM",
	"9C:9E:63": "AVM",

	"00:1A:2B": "Cisco Systems",
	"00:1C:0E": "Cisco Systems",
	"00:23:EA": "Cisco Systems",

	"F4:CF:E2": "TP-Link",
	"50:C7:BF": "TP-Link",
	"EC:17:2F": "TP-Link",
	"B0:48:7A": "TP-Link",
	"C4:6E:1F": "TP-Link",
	"A4:F4:C2": "TP-Link",
	"AC:84:C6": "TP-Link",
	"E8:DE:27": "TP-Link",
	"D8:47:32": "TP-Link",

	"00:1E:58": "Netgear",
	"20:E5:2A": "Netgear",
	"6C:3B:6B": "Netgear",
	"CC:40:D0": "Netgear",
	"A0:04:60": "Netgear",

	"00:1D:0F": "D-Link",
	"1C:7E:E5": "D-Link",
	"C0:A0:BB": "D-Link",
	"B8:A3:86": "D-Link",
	"00:26:B9": "D-Link",

	"00:1D:60": "Belkin",
	"EC:1A:59": "Belkin",
	"94:10:3E": "Belkin",

	"00:1E:10": "Huawei",
	"00:1E:EC": "Huawei",
	"00:25:9E": "Huawei",
	"48:DB:50": "Huawei",
	"70:72:3C": "Huawei",
	"A4:5E:60": "Huawei",
	"00:18:82": "Huawei Technologies",
	"00:22:48": "Huawei Technologies",

	"00:1C:62": "ZTE",
	"00:1E:73": "ZTE",
	"00:26:ED": "ZTE",
	"34:80:B3": "ZTE",
	"E8:65:D4": "ZTE",

	"00:1B:9E": "Sony",
	"00:24:E3": "Sony",
	"FC:0F:E6": "Sony",

	"00:1F:5B": "Nintendo",
	"00:26:59": "Nintendo",
	"7C:BB:8A": "Nintendo",

	"00:17:F2": "Sony Interactive Entertainment",
	"00:24:D7": "Sony Interactive Entertainment",
	"F8:D0:AC": "Sony Interactive Entertainment",

	"00:1C:BF": "Intel Corporate",
	"3C:97:0E": "Intel Corporate",
	"A4:C3:F0": "Intel Corporate",
	"DC:21:48": "Intel Corporate",

	"00:13:20": "Microsoft",
	"00:24:E9": "Microsoft",
	"7C:1E:52": "Microsoft",
	"00:15:5D": "Microsoft Hyper-V",

	"00:50:56": "VMware",
	"00:1C:14": "VMware",

	"52:54:00": "QEMU",
	"08:00:27": "Oracle VirtualBox",
	"00:1C:23": "Citrix Systems"
}

def get_vendor(mac_addr: str) -> str | None:
	mac_addr = mac_addr.upper().replace("-", ":")
	oui = ":".join(mac_addr.split(":")[:3])

	return mac_vendors.get(oui)
