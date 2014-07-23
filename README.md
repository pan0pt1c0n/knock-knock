# KnockdEfault Evaluator v1.1

Author: Justin Hutchens (H@ck1tHu7ch)

KnockdEfault Evaluator - Testing the Perimeter for Default Port Knock Cloaking

Thanks to the developers of Python-libnmap

Proof of concept on my blog - http://www.shortbus.ninja/default-knockd-cloaking-configurations/

## About

This is a simple tool used to determine if a list of remote servers are cloaking any service(s) with the default knockd port knock sequence. 

### Features

 * Mode 1 - Test for cloaked SSH service on TCP port 22
	* This mode is faster but less thorough
	* SSH is the most commonly cloaked service for a few reasons
		* Works as a good fall back when VPN problems impair remote management
		* Often used to remotely manage cloud services that are not managed over VPN
 * Mode 2 - Test all 65,536 ports for cloaked services
	* If default port knock sequence is used for any services, this should find them

## Installation

To install on Kali Linux, merely run the included setup.sh file.

```bash
$ ./setup.sh
```

## Usage

Usage - ./knockdefault.py [Input File] [Output File] [Mode]

Modes:
1) Test SSH Only
2) Test all Services

## Examples

### No Services Opened

In this case, the tool does not discover any services opened with the default knockd port knock sequence

```bash                                          
$ ./knockdefault.py iplist.txt output.txt 2

[-] Scanning 172.16.36.239 with Nmap, this could take a minute...go get some coffee

[-] Sending default knockd sequence to 172.16.36.239

[-] Scanning again...too soon for more coffee???

[-] No new services opened...

```

### Service Opened (HTTP)

In this case, the tool does discover an HTTP service that is activated with the default knockd port knock sequence

```bash  
$ ./knockdefault.py iplist.txt output.txt 2

[-] Scanning 172.16.36.239 with Nmap, this could take a minute...go get some coffee

[-] Sending default knockd sequence to 172.16.36.239

[-] Scanning again...too soon for more coffee???

[+] 1 new ports were opened...
(80, 'tcp')

Writing to output file - output.txt

[-] Disabling opened service on 172.16.36.239 by sending default close sequence...
   *** If you want to manually interact with the service, use the knockd_on-off.py script ***
```
