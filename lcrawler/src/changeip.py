from telnetlib import Telnet
import time

tn = Telnet('127.0.0.1', 9051)
tn.write("AUTHENTICATE\r\n")
tn.read_until("250 OK", 2)
tn.write("signal NEWNYM\r\n")
tn.read_until("250 OK", 2)
tn.write("QUIT\r\n")
tn.close()
print "Tor IP changed!"
