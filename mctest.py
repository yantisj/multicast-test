#!/usr/bin/env python
import time
from datetime import datetime
import socket
import sys
import struct
import argparse
import logging

logger = logging.getLogger('mctest')

group = '232.8.8.8'
mport = 1900
mttl = 6
message = 'multicast test tool'

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='Multicast Send/Receive Test Tool')
parser.add_argument("-send", metavar="string", help="Send a Message",
                    type=str)
parser.add_argument("-receive", help="Receive Messages from Group",
                    action="store_true")
parser.add_argument("-group", metavar="Multicast Group (default: 232.8.8.8)", type=str)
parser.add_argument("-port", metavar="UDP Port", help="UDP Port to receive on (default 1900)")
parser.add_argument('-ttl', metavar='int', help="Multicast TTL (default 6)", type=int)
parser.add_argument("-v", help="Verbose Output", action="store_true")
args = parser.parse_args()

def receiver(group):
    'Receive on a multicast group'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((group, mport))  # use MCAST_GRP instead of '' to listen only
                                # to MCAST_GRP, not all groups on MCAST_PORT
    mreq = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print('Listing on ' + group + ' port ' + str(mport))

    while True:
        (data, address) = sock.recvfrom(1024)
        print ('Received on ' + group + ' from ' + address[0] + \
        ' from port ' + str(address[1]) + ': ' + data)


def sender(group):
    'Send to a multicast group'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, mttl, 32)
    while 1:
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mcast_msg = message + ': ' + time_now
        print('Sending to ' + group + ' (TTL ' + str(mttl) + '): ' + mcast_msg)
        sock.sendto(mcast_msg, (group, mport))
        time.sleep(1)

if args.group:
    group = args.group
if args.ttl:
    mttl = int(args.ttl)
if args.port:
    mport = args.port

if args.send:
    message = args.send
    sender(group)
elif args.receive:
    receiver(group)
else:
    parser.print_help()