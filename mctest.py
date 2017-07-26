#!/usr/bin/env python
import time
from datetime import datetime
import socket
import sys
import struct
import argparse
import logging
import pickle

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', \
                    level=logging.WARNING)

logger = logging.getLogger('mctest')

group = '232.8.8.8'
mport = 1900
mttl = 10
message = 'multicast test tool'

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='Multicast Send/Receive Test Tool')
parser.add_argument("-send", metavar="string", help="Send a Message",
                    type=str)
parser.add_argument("-receive", help="Receive Messages from Group",
                    action="store_true")
parser.add_argument("-group", metavar="Multicast Group (default: 232.8.8.8)", type=str)
parser.add_argument("-port", metavar="UDP Port", help="UDP Port to receive on (default 1900)")
parser.add_argument('-ttl', metavar='int', help="Multicast TTL (default 10)", type=int)
parser.add_argument("-v", help="Verbose Output", action="store_true")
args = parser.parse_args()

def receiver(mgroup):
    'Receive on a multicast group'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Windows workaround
    try:
        sock.bind((mgroup, mport))
    except socket.error:
        sock.bind(('', mport))

    mreq = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print('Listing on ' + mgroup + ' port ' + str(mport))

    while True:
        (data, address) = sock.recvfrom(12000)

        # Try to unpickle log record from a DatagramHandler
        try:
            lrtxt = pickle.loads(data[4:])
            lr = logging.makeLogRecord(lrtxt)
            logger.handle(lr)

        # Print message normally
        except Exception as e:
            print('Exeception', str(e))
            print('Received on ' + mgroup + ' from ' + address[0] + \
            ' from port ' + str(address[1]) + ': ' + data)


def sender(mgroup):
    'Send to a multicast group'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    ttl_bin = struct.pack('@i', mttl)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)
    while 1:
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mcast_msg = message + ': ' + time_now
        print('Sending to ' + mgroup + ' (TTL ' + str(mttl) + '): ' + mcast_msg)
        sock.sendto(mcast_msg, (mgroup, mport))
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
