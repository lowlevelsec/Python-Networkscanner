import random

user_agent_dict = {
	"firefox_windows": [
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:156.0) Gecko/20100101 Firefox/156.0",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:153.0) Gecko/20100101 Firefox/153.0"
	],

	"firefox_macos": [
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 15.8; rv:156.0) Gecko/20100101 Firefox/156.0",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 15.8; rv:153.0) Gecko/20100101 Firefox/153.0"
	],

	"firefox_linux": [
		"Mozilla/5.0 (X11; Linux i686; rv:156.0) Gecko/20100101 Firefox/156.0",
		"Mozilla/5.0 (X11; Linux x86_64; rv:156.0) Gecko/20100101 Firefox/156.0",
		"Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:156.0) Gecko/20100101 Firefox/156.0",
		"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:156.0) Gecko/20100101 Firefox/156.0",
		"Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:156.0) Gecko/20100101 Firefox/156.0",
		"Mozilla/5.0 (X11; Linux i686; rv:153.0) Gecko/20100101 Firefox/153.0",
		"Mozilla/5.0 (Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0",
		"Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:153.0) Gecko/20100101 Firefox/153.0",
		"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0",
		"Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0"
	],

	"firefox_ios": [
		"Mozilla/5.0 (iPhone; CPU iPhone OS 15_8_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/156.0 Mobile/15E148 Safari/605.1.15",
		"Mozilla/5.0 (iPad; CPU OS 15_8_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/156.0 Mobile/15E148 Safari/605.1.15",
		"Mozilla/5.0 (iPod touch; CPU iPhone OS 15_8_0 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) FxiOS/156.0 Mobile/15E148 Safari/605.1.15"
	],

	"firefox_android": [
		"Mozilla/5.0 (Android 17; Mobile; rv:156.0) Gecko/156.0 Firefox/156.0",
		"Mozilla/5.0 (Android 17; Mobile; LG-M255; rv:156.0) Gecko/156.0 Firefox/156.0"
	],

	"chrome_windows": [
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36"
	],

	"chrome_linux": [
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36"
	],

	"chrome_ios": [
		"Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/154.0.8037.55 Mobile/15E148 Safari/604.1",
		"Mozilla/5.0 (iPad; CPU OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/154.0.8037.55 Mobile/15E148 Safari/604.1",
		"Mozilla/5.0 (iPod; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/154.0.8037.55 Mobile/15E148 Safari/604.1"
	],

	"chrome_android": [
		"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.8037.58 Mobile Safari/537.36"
	],

	"edge_windows": [
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36 Edg/154.0.4258.37"
	],

	"edge_macos": [
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36 Edg/154.0.4258.37"
	],

	"edge_android": [
		"Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.8037.58 Mobile Safari/537.36 EdgA/153.0.4234.49",
		"Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.8037.58 Mobile Safari/537.36 EdgA/153.0.4234.49",
		"Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.8037.58 Mobile Safari/537.36 EdgA/153.0.4234.49",
		"Mozilla/5.0 (Linux; Android 10; ONEPLUS A6003) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.8037.58 Mobile Safari/537.36 EdgA/153.0.4234.49"
	],

	"edge_ios": [
		"Mozilla/5.0 (iPhone; CPU iPhone OS 18_7_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/27.0 EdgiOS/153.4234.46 Mobile/15E148 Safari/605.1.15"
	],

	"safari_macos": [
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 15_8_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/27.0 Safari/605.1.15",
	],

	"safari_ios": [
		"Mozilla/5.0 (iPhone; CPU iPhone OS 18_7_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/27.0 Mobile/15E148 Safari/604.1",
		"Mozilla/5.0 (iPad; CPU OS 18_7_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/27.0 Mobile/15E148 Safari/604.1",
		"Mozilla/5.0 (iPod touch; CPU iPhone 18_7_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/27.0 Mobile/15E148 Safari/604.1"
	],

	"opera_windows": [
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36 OPR/137.0.0.0",
		"Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36 OPR/137.0.0.0"
	],

	"opera_macos": [
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 15_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36 OPR/137.0.0.0"
	],

	"opera_linux": [
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36 OPR/137.0.0.0"
	],

	"opera_huawei": [
		"Mozilla/5.0 (Linux; Android 10; VOG-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.8037.58 Mobile Safari/537.36 OPR/76.2.4027.73374"

	],

	"opera_samsung": [
		"Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.8037.58 Mobile Safari/537.36 OPR/76.2.4027.73374",
		"Mozilla/5.0 (Linux; Android 10; SM-N975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.8037.58 Mobile Safari/537.36 OPR/76.2.4027.73374"
	]
}

def random_user_agent() -> tuple[str, str]:
	browser_os = random.choice(list(user_agent_dict))
	user_agent = random.choice(user_agent_dict[browser_os])

	return browser_os, user_agent
