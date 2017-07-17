# Multicast Test Tool in Python2/3

```
$ ./mctest.py
usage: mctest.py [-h] [-send string] [-receive]
                 [-group Multicast Group default: 232.8.8.8] [-port UDP Port]
                 [-ttl int] [-v]

Multicast Send/Receive Test Tool

optional arguments:
  -h, --help            show this help message and exit
  -send string          Send a Message
  -receive              Receive Messages from Group
  -group Multicast Group (default: 232.8.8.8)
  -port UDP Port        UDP Port to receive on (default 1900)
  -ttl int              Multicast TTL (default 10)
  -v                    Verbose Output
```

## Receive Example (uPNP Traffic)
```
$ ./mctest.py -rec -group 239.255.255.250 -port 1900
Listing on 239.255.255.250 port 1900
Received on 239.255.255.250 from 10.26.73.211 from port 1900: NOTIFY * HTTP/1.1
HOST: 239.255.255.250:1900
CACHE-CONTROL: max-age=60
LOCATION: http://10.26.73.211:6432/description.xml
NT: upnp:rootdevice
NTS: ssdp:alive
SERVER: lwIP/1.3.2
USN: uuid:upnp_MDL-S2E-c0a26d004ba8::upnp:rootdevice
```

## Send Example with Receive
```
./mctest.py -send 'test from imac'
Sending to 232.8.8.8 (TTL 10): test from imac: 2017-07-17 11:23:29
Sending to 232.8.8.8 (TTL 10): test from imac: 2017-07-17 11:23:30
Sending to 232.8.8.8 (TTL 10): test from imac: 2017-07-17 11:23:31
```

### Receiver
```
./mctest.py -rec
Listing on 232.8.8.8 port 1900
Received on 232.8.8.8 from 128.23.200.25 from port 51596: test from imac: 2017-07-17 11:23:29
Received on 232.8.8.8 from 128.23.200.25 from port 51596: test from imac: 2017-07-17 11:23:30
Received on 232.8.8.8 from 128.23.200.25 from port 51596: test from imac: 2017-07-17 11:23:31
```
