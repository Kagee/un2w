import socket
import sys
import pynmea2
import time
from geojson import FeatureCollection, Feature, LineString

#CONFIG
USERS=[("hildenae","htconem8"),("hildenæ","htcone m8!")]

UDP_IP = "0.0.0.0"
UDP_PORT = 11109

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

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
        from geojson import LineString
        ls = LineString([(float("%.6f" % msg.latitude), float("%.6f" % msg.longitude))])
        print (ls)
        sys.stdout.flush()
    except UnicodeError as ue:
        print("Discarding, failed to decode as UTF-8: %s (%s)" % (data, ue), file=sys.stderr)
        continue
    except ValueError as ve:
        print (ve, file=sys.stderr)
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
