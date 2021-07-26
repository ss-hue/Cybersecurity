#!/usr/bin/env python3

import sys, os, re
import subprocess
import time



hdict = {}

host = subprocess.Popen(["arp -a | egrep -o '[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,2}'"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

host_out = host.communicate()[0].decode("ascii").split()


#print(host_out)

for host in host_out:
    
    if "192" in host:
        
        #print("sudo nmap -O {}".format(host))
        nmap = subprocess.Popen(["sudo nmap -O {}".format(host)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #output is str type.
        output = nmap.communicate()[0].decode("ascii")
        hdict[host] = re.search("MAC Address: .*", output)
        print(output)



        

for ip, mac in hdict.items():
    if mac is not None:
        print("{} belongs to {}".format(ip, mac.group())) 

