from telnetlib import Telnet
import time, sys

# for i in range(9060, 9066):
i = sys.argv[1]
serverIP = os.environ['OPENSHIFT_PYTHON_IP'] if ('OPENSHIFT_PYTHON_IP' in os.environ) else '127.0.0.1'
tn = Telnet(serverIP, i)
tn.write("AUTHENTICATE\r\n")
tn.read_until("250 OK", 2)
tn.write("signal NEWNYM\r\n")
tn.read_until("250 OK", 2)
tn.write("QUIT\r\n")
tn.close()
print "Tor IP for port %d changed!" % i
