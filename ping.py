#! puthon3
# ping specific hosts from a txt file

import sys
import os
import nmap
from colorama import init, Back
init()


scriptDir = sys.path[0]
hosts = os.path.join(scriptDir, 'hosts.txt')
try:
    hostsFile = open(hosts, "r")
except FileNotFoundError:
    print("File not found!", sys.exc_info()[0])
    sys.exit(1)
lines = hostsFile.readlines()

try:
    nm = nmap.PortScanner()
except nmap.PortScannerError:
    print('Nmap not found', sys.exc_info()[0])
    sys.exit(1)
except:
    print("Unexpected error:", sys.exc_info()[0])
    sys.exit(1)

def ping(current_host):
    nm.scan(current_host, arguments='-sP')
    if (len(nm.all_hosts()) != 0):
        print(Back.GREEN + str(current_host).ljust(25, '.') + 'UP  ')
    else:
        print(Back.RED + str(current_host).ljust(25, '.') + 'DOWN')

while True:
    for host in lines:
        ping(host.strip())
    print('='.ljust(29, '='))
