# Tcp Chat server
# Last revision: Jan 21, 2015

# To-do:
# - when someone disconnects, socket number changes and PM could go to the wrong person!
 
import socket, select

def get_username(sock):
    """ Returns a username of given socket, if there is any.
    """
    try:
        username = user_dict[sock.getpeername()]
    except:
        username = sock.getpeername()

    return str(username)

def generate_username(user_dict, default_username = 'user'):
    """ Generate a generic username when it is not supplied by chat client.
    """

    count = 1
    while 1:
        username = default_username+"_"+str(count)
        if not username in user_dict.itervalues():
            return username
        else:
            count += 1

 
def broadcast_data (sock, message):
    """ Broadcast chat messages to all connected clients.
    """
    
    msg_spl = message.split('\\')

    # SERVER COMMANDS
    # \help -print help
    # \exit - disconnect
    # \users - print connected users
    # \user_num message - send that usear a private message
    
    # Handle server commands
    if len(msg_spl) > 1:

        soc_no = msg_spl[-1].strip()

        # Disconnect if -1#
        if soc_no == 'exit':
            disconnect_user(sock)
            return 0

        if soc_no == 'help':
            sock.send("\r\n\users - retrieve current user list\n")
            sock.send("\r\user_no message - send a private message\n")
            sock.send("\r\exit - disconnect\n")
            return 0

        # Add username to dictionary
        if "$user_init" in soc_no:
            soc_no = soc_no.split()
            username = " ".join(soc_no[1:])

            # Check if username already exists
            if not username in user_dict.itervalues():
                user_dict[sock.getpeername()] = generate_username(user_dict) if username  == '000' else username
            else:
                # Generate new random username
                username = generate_username(user_dict)
                sock.send("\rYour requested username already exist on the server! You are logged in as: "+username+"\n")
                user_dict[sock.getpeername()] = username

            print get_username(sockfd)+" entered room\n"
            broadcast_data(sock, "$server_sys "+get_username(sockfd)+" entered room\n")

            return 0

        # Return list of connected users
        if soc_no == 'users':
            sock.send("\r\nTo send a private message, type user_number# message\n")
            sock.send("\re.g. \\2 How you doin'?\n")
            sock.send("\rConnected users:\n\n")
            for i, socket in enumerate(CONNECTION_LIST):
                if socket != server_socket:
                    username = get_username(socket)
                    # Print out all connected users to the user that requested the list
                    sock.send("\r\\"+str(i)+" "+str(username)+'\n')

            return 0

        # Split soc_no to private message, if any
        try:
            soc_no = soc_no.split()

            if len(soc_no) > 1:
                PM_message = " ".join(soc_no[1:])+"\n"
            else:
                PM_message = ""

            soc_no = int(soc_no[0])
        except:
            return 0


        # Send PM
        if soc_no < len(CONNECTION_LIST):
            socket = CONNECTION_LIST[soc_no]
            username = get_username(sock)
            message = "\r" + 'PM<' + str(username) + '> ' + PM_message
        else:
            sock.send("\rNo user with that number!\n")
            return 0
        

        try :
            socket.send(message) 
        except :
            # broken socket connection may be, chat client pressed ctrl+c for example
            socket.close()
            CONNECTION_LIST.remove(socket)

        return 0

    # Send message to all users
    for socket in CONNECTION_LIST:
        #Do not send the message to master socket and the client who has send us the message
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)

def disconnect_user(sock):
    """ Disconnects user with given socket.
    """
    addr = sock.getpeername()

    disconnect_message = "$server_sys Client "+get_username(sock)+" is offline\n"
    broadcast_data(sock, disconnect_message)
    disconnect_message = " ".join(disconnect_message.split()[1:])+"\n"
    print disconnect_message

    # Remove user from list, if any
    try:
        del user_dict[sock.getpeername()]
    except:
        pass

    # Remove socket
    CONNECTION_LIST.remove(sock)

    sock.close()



 
if __name__ == "__main__":
     
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 8080
     
    # Dictionary of users
    user_dict = {}

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            # New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
             
            # Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    # In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)

                    # Get username, if provided
                    username = get_username(sock)

                    if data:
                        broadcast_data(sock, "\r" + '<' + str(username) + '> ' + data)               
             
                except:
                    disconnect_user(sock)
                    continue
     
    server_socket.close()