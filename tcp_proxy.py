import sys
import socket
import threading

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server.bind((local_host, local_port))
    except:
        print "[!!] Failed to listen on %s%d" % (local_host, local_port)
        print "[!!] Check for other listening sockets ot correct permissions"
        sys.exit(0)
        
    print "[*] Listening on %s%d" % (local_host, local_port)
    
    server.listen(5)
    
    while True:
        client_socket, addr = server.accept()
        
        #print out the local connection information
        print "[==>] Recieved incoming connection from %S%D" % (addr[0], addr[1])
        
        #start a thread to talk to the remote host
        proxy_thread = threading.Thread(target=proxy_handler, 
                                        args=(client_socket,
                                              remote_host,
                                              remote_port,
                                              receive_first))
        proxy_thread.start()

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    
    #connect to the remote host
    remote_socket = socket.socket(socket.AF_INET, 
                                  socket.SOCK_STREAM)
    remote_socket.connect((remote_host,remote_port))
    
    #receive data from the remote end if necessary
    if receive_first:
        
        remote_buffer =recieve_from(remote_sockt)
        hexdump(remote_buffer)
        
        #send it to our response handler
        remote_buffer = response_handler(remote_buffer)
        
        #if we have data to send to our local client, send it
        if len(remote_buffer):
            print "[<==] Sending %d bytes to localhost." % len(remote_buffer)
            client_socket.send(remote_buffer)
            
        #now lets loop and read from local, send to remote, sned to local
        #rinse, wash, repeat
        while True:
            
        
    
def main():
    
    #no fancy command linle parsing this time!!!
    if len(sys.argv[1:]) !=5:
        print "Usage: ./proxy.py [localhost] [localport] [remotehost]\
        [remoteport] [receive_first]"
        print "Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True"
        sys.exit(0)
    
    #set up local listening parameters
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    
    #setup remote target
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    
    #this tells our proxy to connect and receive data
    #before sending to the remote host
    receive_first = sys.argv[5]
    
    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False
    
    #now spin up our listening socket
    server_loop(local_host,local_port,
                remote_host,remote_port,
                receive_first)

main()
