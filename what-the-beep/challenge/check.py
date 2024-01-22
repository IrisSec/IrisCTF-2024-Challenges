#!/usr/bin/env python3

import random
import time

print("Where did the beep originate from? Provide coordinates. Use WGS 84/Pseudo-Mercator")
print("projection (aka what Google Maps uses). Please separate your coordinates with a comma.")
print("Example input (The White House): 38.897288, -77.036547")
print("If your answer is within an acceptable range, you will get the flag.")
print()

answer = input("Input: ")

print("Checking your answer...")

time.sleep(random.uniform(0, 3))

try:
	ca, cb = answer.split(",")
	ca = float(ca)
	cb = float(cb)
	if (ca > 37.273 and ca < 37.274) and (cb > -120.326 and cb < -120.324):
		with open("flag.txt", "r") as f:
			flag = f.read()
		print("\n"+flag.strip())
	else:
		print("\nNot exactly! Check your work and try again.")
except:
	print("\nYou did something unexpected.")

print("Done.")
