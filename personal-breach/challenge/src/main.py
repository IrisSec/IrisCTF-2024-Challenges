#!/usr/bin/env python3

import os
import sys

from app import *

APP_NAME = "osint.2"

# Positional arguments.
P_ARGUMENTS = {
	("<IP>",)    : "Server bind IPv4 address (default=\"0.0.0.0\").",
	("<PORT>",)  : "Server bind port number (default=8080).",
}

# Optional help arguments.
H_ARGUMENTS = {
	("-h", "--help"): "Display the help menu and exit.",
}

# Optional arguments.
O_ARGUMENTS = {
	("-d",): "Enable debugging mode.",
}

def print_help(path: str="main.py", alignmentWidth: int=16) -> None:
	"""
	Output help menu to stdout upon request. LHS args are aligned to a fixed
	width of alignmentWidth columns.
	"""

	# Shorthand alignment function for aligning to the alignmentWidth.
	align = lambda s: s + ' '*(alignmentWidth-len(s))

	print(f"Usage: {path} [ARGUMENTS] <IP> <PORT>")
	print(f"Start the {APP_NAME} web application interface.")
	print()

	print("Help:")
	for key in H_ARGUMENTS:
		print(align(", ".join([*key])) + H_ARGUMENTS[key])

	print("Positional arguments:")
	for key in P_ARGUMENTS:
		print(align(", ".join([*key])) + P_ARGUMENTS[key])

	print("Optional arguments:")
	for key in O_ARGUMENTS:
		print(align(", ".join([*key])) + O_ARGUMENTS[key])

def main(args: list=["./main.py"]):

	path = args[0]
	args = args[1::]

	settings = {
		"host"   : "0.0.0.0",
		"port"   : 1337,
		"debug"  : False,
	}

	# Parsing help arguments.
	if any([arg in list(*H_ARGUMENTS.keys()) for arg in args]):
		print_help(path)
		return 0

	# Parsing debug arguments.
	if any([arg == "-d" for arg in args]):
		try:
			settings["debug"] = True
			args.remove("-d")
		except:
			pass

	# Parsing conditional arguments.
	try:
		settings["host"] = args.pop(0)
		settings["port"] = args.pop(0)
	except:
		pass

	app.run(**settings)

if __name__ == "__main__":
	main(sys.argv[0::])
