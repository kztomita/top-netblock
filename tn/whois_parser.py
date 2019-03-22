import re
import netaddr

def get_cidr(text):
    m = re.search('cidr:\s*([0-9.]+/\d+)', text, re.I)
    if m:
        return m.group(1)

    m = re.search('netrange:\s*([0-9.]+)\s*-\s*([0-9.]+)', text, re.I)
    if m:
        cidrs = netaddr.iprange_to_cidrs(m.group(1), m.group(2))
        return str(cidrs[0])

    return None

def get_netname(text):
    m = re.search('netname:\s*(.+)', text, re.I)
    if m:
        return m.group(1)
    return None

def parse(text):
    cidr = get_cidr(text)
    netname = get_netname(text)
    return {
        'cidr': cidr,
        'netname': netname,
    }
