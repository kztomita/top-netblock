import sys
import ipaddress
import re
import netaddr
import tn.whois
import tn.whois_parser

netblocks = []
netnames = {}

def lookup_netblock(ip):
    for netblock in netblocks:
        if ip in netblock['network']:
            return netblock
    return None

def read_ip(line):
    ip = ipaddress.ip_address(line)
    if not ip.is_global:
        print("{} is not global address.".format(ip))
        return None

    netblock = lookup_netblock(ip)
    if netblock is not None:
        return netblock

    result = tn.whois.get(str(ip))
    whois_data = tn.whois_parser.parse(result)
    if whois_data['cidr'] is None:
        print("{}: Can't get cidr.".format(ip))
        return None
    if whois_data['netname'] is None:
        print("{}: Can't get netname.".format(ip))
        return None

    print('Found {}'.format(whois_data))

    netblock = {
        'network': ipaddress.ip_network(whois_data['cidr']),
        'netname': whois_data['netname'],
        'count': 0,
    }
    netblocks.append(netblock)

    return netblock

def main():
    for line in sys.stdin:
        line = line.rstrip()
        if line == '':
            continue

        netblock = read_ip(line)
        if netblock is None:
            continue

        netblock['count'] += 1

        netname = netblock['netname']
        if netname not in netnames:
            netnames[netname] = 0
        netnames[netname] += 1

    print('\n\nFounded netblocks')
    for n in sorted(netblocks, key=lambda x: x['count'],reverse=True):
        print('{}: {}'.format(n['network'], n['count']))

    print('\nFounded netnames')
    for n in sorted(netnames.items(),  key=lambda x: x[1], reverse=True):
        print('{}: {}'.format(n[0], n[1]))

if __name__ == "__main__":
    main()
