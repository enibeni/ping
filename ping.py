#! puthon3
# ping specific hosts from a txt file

import sys
import os
import nmap
from colorama import init, Back

init()


def check(current_host, port=None, service=None):
    try:
        nm = nmap.PortScanner()
    except nmap.PortScannerError:
        print('Nmap not found', sys.exc_info()[0])
        sys.exit(1)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit(1)
    if port is None:
        nm.scan(current_host, arguments='-sP')
        if len(nm.all_hosts()) != 0:
            print(Back.GREEN + str(current_host).ljust(25, '.') + 'UP  ' + Back.BLACK + service)
        else:
            print(Back.RED + str(current_host).ljust(25, '.') + 'DOWN ' + Back.BLACK + service)
    else:
        nm.scan(current_host, str(port))
        port_state = nm[str(nm.all_hosts()).strip('[]\'\'')]['tcp'][int(port)]['state']
        if port_state == 'open':
            print(Back.GREEN + str(current_host) + ':' + port.ljust(12, '.') + 'UP  ' + Back.BLACK + service)
        else:
            print(Back.RED + str(current_host) + ':' + port.ljust(12, '.') + 'DOWN' + Back.BLACK + service)


def parse(line):
    try:
        result = dict(x.split(':') for x in line.split(' '))
    except ValueError:
        print("Can't parse the file", sys.exc_info()[0])
        sys.exit(1)
    return result


def read_file():
    scriptDir = sys.path[0]
    hosts = os.path.join(scriptDir, 'hosts.txt')
    try:
        hostsFile = open(hosts, "r")
    except FileNotFoundError:
        print("File not found!", sys.exc_info()[0])
        sys.exit(1)
    return hostsFile.readlines()


def ping():
    lines = read_file()
    for line in lines:
        if not line.startswith('#'):    #comment in txt file
            dict = parse(line.strip())
            current_host = dict['host']
            if 'port' in dict:
                port = dict['port']
            else:
                port = None
            if 'service' in dict:
                service = dict['service']
            else:
                service = ''
            check(current_host, port, service)
    print('='.ljust(29, '='))


while True:
    ping()
