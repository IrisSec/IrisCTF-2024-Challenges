#!/usr/bin/env python3

import time
from dnserver import DNSServer

print("Starting DNS server.")

server = DNSServer.from_toml('example_zones.toml', port=53)
server.start()
assert server.is_running

while True:
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		print("\n\nStopping DNS server.")
		server.stop()
		exit(0)
