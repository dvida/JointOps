""" Backed for the client application that handles server communication.
"""

import sys
import socket
import select
import threading

class ClientBackend():
    def __init__(self, screen_app):
        self.screen_app = screen_app
        self.disconnect_flag = False
        self.host = None
        self.port = None

    def connect(self, host, port, username = None):
        """ Connect to server, given IP, port and username (optional).
        """

        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sock.settimeout(1)
        
         
        # Connect to remote host
        try:
            self.sock.connect((self.host, self.port))
        except:
            # Unable to connect
            return False

        # Send username
        if username == None:
            username = '$no_username'

        self.sock.send("\\$user_init "+str(username))

        return True

    def sendMessage(self, message):
        """ Send message to server.
        """
        if not self.disconnect_flag:
            self.sock.send(message)

    def disconnectServer(self):
        """ Close socket and disconect.
        """

        # Close socket by connecting to it, triggering shutdown procedure
        self.disconnect_flag = True
        self.sock.send("\\exit")
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def startListen(self):
        """ Run the startListenThread in another thread.
        """
        self.listen_thread = threading.Thread(target=self.startListenThread)
        self.listen_thread.daemon = True
        self.listen_thread.start()


    def startListenThread(self):
        """ Start listening for server messages.
        """

        while 1:

            if self.disconnect_flag:
                break

            socket_list = [self.sock]
             
            # Get the list sockets which are readable
            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
             
            for temp_sock in read_sockets:
                if self.disconnect_flag:
                    break
                # Incoming message from remote server
                if temp_sock == self.sock:
                    try:
                        data = temp_sock.recv(4096)
                    except:
                        data = False
                    if not data :
                        self.screen_app.addLine('Disconnected from chat server\n')
                        
                        self.disconnect_flag = True
                        self.screen_app.connected_flag = False

                        temp_sock.shutdown(socket.SHUT_RDWR)
                        temp_sock.close()
                        sys.exit(0)

                    else :
                        # Print data
                        if '$server_sys' in data:
                            data = "\nSystem: "+" ".join(data.split()[1:])+"\n"

                        self.screen_app.addLine(data)

