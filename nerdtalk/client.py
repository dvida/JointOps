# Client
import socket, select, string, sys
import threading
 
def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()

def read_stdin(s):
    global exit_program
    while 1:
        if exit_program:
            break
        msg = sys.stdin.readline()
        s.send(msg)
        prompt()

def read_socket(s):
    global exit_program
    while 1:
        if exit_program == True:
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
                    exit_program = True
                    #sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    prompt()
 
exit_program = False
#main function
if __name__ == "__main__":

    username = '000'
     
    if(len(sys.argv) < 3) :
        print 'Usage : python telnet.py hostname port username'
        sys.exit()
     
    host = sys.argv[1]
    port = int(sys.argv[2])

    if(len(sys.argv) == 4):
        username = sys.argv[3]  # Get username argument if present

     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host. Start sending messages'

    # Send username
    s.send("\r$user_init#"+str(username))

    prompt()
     
    
    soc_thread = threading.Thread(target=read_socket, args = (s,))
    stdin_thread = threading.Thread(target=read_stdin, args = (s,))

    soc_thread.start()
    stdin_thread.start()


    stdin_thread.join()
    soc_thread.join()


        