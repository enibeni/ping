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

# 9915
# 9911

try:
    nm = nmap.PortScanner()
except nmap.PortScannerError:
    print('Nmap not found', sys.exc_info()[0])
    sys.exit(1)
except:
    print("Unexpected error:", sys.exc_info()[0])
    sys.exit(1)

def ping(current_host, port=None):
    if port is None:
        nm.scan(current_host, arguments='-sP')
        if len(nm.all_hosts()) != 0:
            print(Back.GREEN + str(current_host).ljust(25, '.') + 'UP  ')
        else:
            print(Back.RED + str(current_host).ljust(25, '.') + 'DOWN')
    else:
        nm.scan(current_host, str(port))
        port_state = nm[str(nm.all_hosts()).strip('[]\'\'')]['tcp'][int(port)]['state']
        if port_state == 'open':
            print(Back.GREEN + str(current_host) + ':' + port.ljust(12, '.') + 'UP  ')
        else:
            print(Back.RED + str(current_host) + ':' + port.ljust(12, '.') + 'DOWN')

while True:
    for line in lines:
        params = line.split(':')
        if len(params) == 1:
            ping(params[0].strip())
        else:
            ping(params[0], params[1].strip())
    print('='.ljust(29, '='))