import socket
import sys
import pynmea2
import time
from geojson import FeatureCollection, Feature, LineString
from collections import deque
import os.path
#CONFIG
USERS=[("hildenae","htconem8"),("hildenæ","htcone m8!")]

UDP_IP = "0.0.0.0"
UDP_PORT = 11109

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

l = deque([], 1000)

run = True
while run:
    try:
	# 1024-82 (NMEA max) - 2 (two /) = 940 bytes for Account_ID and Device ID 
        data, addr = sock.recvfrom(1024)
        s = data.decode("utf-8")
        if (s.count("/") != 2):
            raise ValueError("Wrong number of / in input data: %s" % (s))
        acc, dev, nmea = s.split('/')
        msg = pynmea2.parse(nmea)
        print (msg.timestamp, msg.latitude, msg.longitude)
        t = (float("%.6f" % msg.latitude), float("%.6f" % msg.longitude))
        ls = LineString([t])
        l.append(t)
        print (ls)
        #print (FeatureCollection(Feature(LineString(list(l)))))
        fn = "%s-%s.json" % (acc, dev)
        #if (os.path.isfile(fn)):
        #    print(fn, "exsists")
        #else:
        #    print(fn, "dontnt exsists")
        f = open(fn, 'w')
        print (FeatureCollection([Feature("line1", LineString(list(l)))]), file=f)
        f.close()
        sys.stdout.flush()
    except UnicodeError as ue:
        print("Discarding, failed to decode as UTF-8: %s (%s)" % (data, ue), file=sys.stderr)
        continue
    except ValueError as ve:
        print ("%s: (%s)" %(ve, s), file=sys.stderr)
        continue
    except pynmea2.nmea.ParseError:
        print("Discarding, failed to parse NMEA: ", s, file=sys.stderr)
        continue
    except KeyboardInterrupt:
        print("KeyboardInterrupt received, cleaning …", file=sys.stderr)
        #sock.shutdown(socket.SHUT_WR) # (maybe not close socket?)
        run = False
        # close file handles ?
    except:
        print ("Unexpected error:", sys.exc_info()[0], file=sys.stderr)
        raise
