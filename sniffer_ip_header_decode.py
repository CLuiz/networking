import socket
import os
import struct
from ctypes import *

#host to listen on
host = '192.168.0.187'

#our IP header

class IP(Structure):
    _fields = [
        ("ihl",          c_ubyte,4),
        ("version"       c_ubyte,4),
        ("tos"           c_ubyte),
        ("len"           c_ushort),
        ("id"            c_ushort),
        ("offset"        c_ushort),
        ("ttl"           c_ubyte),
        ("protocol_num"  c_ubyte),
        ("sum"           c_ushort),
        ("src",          c_ulong),
        ("dst",          c_ulong)
        ]
    
    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer=None):
        
        # map protocol constants to theor names
        self.protocol_map = {1:"ICMP", 6:"TCP", 17: "UDP"}
        
        #human readable IP addresses
        