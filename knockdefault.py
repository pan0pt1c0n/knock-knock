#!/usr/bin/python

from scapy.all import *
from libnmap.process import NmapProcess
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser
import sys

if len(sys.argv) != 4:
	print "\n\n          *** Knockd Evaluator ***          "
	print "To test systems for default knockd configuration\n"
	print "Usage - ./knockd_eval.py [Input File] [Output File] [Mode]"
	print "----------"
	print "\nModes:\n1) Test SSH Only\n2) Test all Services\n"
	print "Example - ./knockd_eval.py iplist.txt 2"
	print "Example will test default knockd sequence to identify opened services for all ports on systems listed in input file"
	print "----------\n"
	sys.exit()

def knockd_test(ip,outfile,start_key,stop_key,mode):
	## Baseline Nmap Scan
	print "\n[-] Scanning " + ip + " with Nmap, this could take a minute...go get some coffee"
        if str(mode) == '1':
		nm = NmapProcess(ip, options="-p 22")
		rc = nm.run()
		if nm.rc == 0:
			before = NmapParser.parse(nm.stdout)
			before_ports = before.hosts[0].get_ports()
		else:
			print nm.stderr
			sys.exit()
	elif str(mode) == '2':
		nm = NmapProcess(ip, options="-p 0-65535")
                rc = nm.run()
                if nm.rc == 0:
                        before = NmapParser.parse(nm.stdout)
                        before_ports = before.hosts[0].get_ports()
                else:
                        print nm.stderr
                        sys.exit()
	else:
		print "\n[-] An error has occured"
		sys.exit()

	## Sending Default Knockd Port Knock Sequence with Scapy
        print "\n[-] Sending default knockd sequence to " + ip
        for x in start_key:
                send(IP(dst=ip)/TCP(dport=x),verbose=0)

	## Subsequent Nmap Scan
	print "\n[-] Scanning again...too soon for more coffee???"
	rc = nm.run()
	if nm.rc == 0:
		after = NmapParser.parse(nm.stdout)
		after_ports = after.hosts[0].get_ports()
	else:
		print nm.stderr
		sys.exit()
	
	## Compare Scans to Determine if any Services were Activated
	diff = set(after_ports)-set(before_ports)
	new_ports = list(diff)
	if len(new_ports) > 0:
		print "\n[+] " + str(len(new_ports)) + " new port(s) opened..."
		for x in new_ports:
			print x
		print "\nWriting to output file - " + outfile
                f = open(outfile,'a')
                f.write("Ports opened on " + ip + " - " + str(new_ports) + "\n")
		f.close()
	
	## Stopping Activated Services with Default Close Sequence
		print "\n[-] Disabling opened service on " + ip + " by sending default close sequence..."
		print "   *** If you want to manually interact with the service, use the knockd_on-off.py script ***\n"
        	for x in stop_key:
                	send(IP(dst=ip)/TCP(dport=x),verbose=0)
	elif len(new_ports) == 0:
		print "\n[-] No new services opened...\n"
	else:
		print "\n[-] An error has occurred"
		sys.exit()

## Default start and stop knockd port knock sequences
start_key = (7000,8000,9000)
stop_key = (9000,8000,7000)

## Arguments supplied
ip_list = sys.argv[1]
outfile = sys.argv[2]
mode = sys.argv[3]

## Execution of function
for ip in open(ip_list).readlines():
	knockd_test(ip.strip(),outfile,start_key,stop_key,mode)
