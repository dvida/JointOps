# Tcp Chat server
 

import socket, select, string, sys
import threading
 
#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)

    print message
    try:
        s.send(message)
    except:
        pass


def server_fnc():
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
                 
                broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)
             
            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)               
                 
                except:
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()

def read_stdin(s):
    while 1:
        if not soc_thread.isAlive():
            break
        msg = sys.stdin.readline()
        s.send(msg)
        prompt()

def read_socket(s):
    exit_while = False
    while 1:
        if exit_while == True:
            break
        #socket_list = [sys.stdin, s]
        socket_list = [s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    exit_while = True
                    #sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    prompt()

 
if __name__ == "__main__":

    # Connect to other server
    if(len(sys.argv) < 3) :
        print 'Usage : python telnet.py hostname port'
        sys.exit()
     
    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
        print 'Connected to:', host, 'on', port

        soc_thread = threading.Thread(target=read_socket, args = (s,))
        stdin_thread = threading.Thread(target=read_stdin, args = (s,))
        soc_thread.start()
        stdin_thread.start()


    except :
        print 'Unable to connect'
        #sys.exit()

    prompt()
     
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 8889
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    server_thread = threading.Thread(target=server_fnc, args = ())
    

    server_thread.start()
    
    server_thread.join()

        
    stdin_thread.join()
    soc_thread.join()
     
    server_socket.close()