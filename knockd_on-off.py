#!/usr/bin/python

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import sys

if len(sys.argv) != 3:
	print "Usage - ./knock_switch.py [on/off] [IP Address]"
	print "Example - ./knock_switch.py on 127.0.0.1"
	print "Example will activate knockd linked service on 127.0.0.1"
	sys.exit()

start_key = (7000,8000,9000)
stop_key = (9000,8000,7000)

status = sys.argv[1]
ip = sys.argv[2]

if (status == 'on'):
	key=start_key
elif (status == 'off'):
	key=stop_key
else:
	print "Invalid Input"
	sys.exit()

for x in key:
	send(IP(dst=ip)/TCP(dport=x),verbose=0)
