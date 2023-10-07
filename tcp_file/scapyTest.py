import sys
from scapy.all import *

while True:
    sniff(iface="Wi-Fi", prn = lambda x:x.show())