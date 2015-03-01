""" Console user interface for the Client application.
"""

import curses
from curses.textpad import Textbox, rectangle
import sys
import client_backend

class Screen():
    def __init__(self, stdscr):
        self.stdscr = stdscr

        self.personal_prefix = '<You> '


        self.client_net = None
        self.connected_flag = False

        # Set screen attributes
        self.stdscr.nodelay(1) # this is used to make input calls non-blocking

        curses.noecho()
        curses.curs_set(1) # 1 - show cursor, 0 - hide cursor
        screen.keypad(1)

        self.rows, self.cols = self.stdscr.getmaxyx()
        self.message_lines = []

        # Create custom colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

        # Init entry box

        bottom_line = self.rows - 1

        self.text_height = 1
        self.text_width = self.cols-3
        self.text_top = bottom_line - self.text_height - 3
        self.text_left = 1

        self.editwin = curses.newwin(self.text_height,self.text_width, self.text_top, self.text_left)

        # Init textbox entry
        self.box = Textbox(self.editwin)

        # Write host on the top of the screen
        self.updateHeader("NerdTalk")

        # Draw rectangle
        self.drawEntryRectangle()

        # Init message pad
        ## Determine maximum lines visible on the message pad before shifting
        self.mgs_lines_start = 1
        self.msg_lines_end = self.rectangle_top - 1
        self.message_row_size = self.msg_lines_end - self.mgs_lines_start

        self.message_pad = curses.newpad(self.msg_lines_end - self.mgs_lines_start, self.text_width)
        
        self.message_pad.refresh(0, 0, self.mgs_lines_start, 0, self.message_row_size, self.text_width)

        # Print welcome message
        self.printWelcome()

        # Start entry box
        self.entryBox()

    def drawEntryRectangle(self):
        """ Draws entry rectangle on the screen.
        """
        self.rectangle_top = self.text_top - 1
        rectangle_left = self.text_left - 1
        rectangle_bottom = self.rectangle_top + self.text_height + 2
        rectangle_right = rectangle_left + self.text_width + 2

        rectangle(self.stdscr, self.rectangle_top, rectangle_left, rectangle_bottom, rectangle_right)

        self.stdscr.refresh()


    def updateHeader(self, header):
        """ Updates the header text.
        """
        host_center = (self.cols-1)/2 - len(header)/2 - 1
        self.stdscr.addstr(0, host_center, header, curses.color_pair(1))

        self.drawEntryRectangle()

    def updateStatusBar(self):
        """ Updates status bar line.
        """

        users_no = str(0)
        self.stdscr.addstr(self.rows-1, 0, ('Connected users: %4s' % str(users_no)), curses.color_pair(1))

        self.drawEntryRectangle()

    def connectServer(self, cmd_args):
        """ Connects to a server given the host, port and username (optional).
        """

        # Check if alredy connected
        if self.connected_flag:
            self.addLine("You are already connected!\n")
            return 0

        if len(cmd_args) < 2:
            self.addLine("To connect to a server:\n\\connect IP port username\n")
            return 0

        elif len(cmd_args) == 2:
            username = None
        else:
            username = cmd_args[2]

        host, port = cmd_args[0:2]

        # Start client backend (handles server connections)
        self.client_net = client_backend.ClientBackend(self)

        # Connect to server
        if self.client_net.connect(host, int(port), username):
            self.connected_flag = True
            self.client_net.startListen()

            self.addLine("Connection success!\n")
            self.updateHeader("NerdTalk - connected to: "+host)

        else:
            # Connection failed
            self.addLine("Error: Could not connect to server!\n")

    def disconnectServer(self):
        """ Disconnect from the current server.
        """

        if not self.connected_flag:
            self.addLine("You are not connected no any server!\n")
            return 0

        self.client_net.disconnectServer()
        self.connected_flag = False
        self.addLine("Disconnected!")
        self.updateHeader("NerdTalk")

        del self.client_net



    def handleCommands(self, command):
        """ Handles commands starting with backslash.
        """

        command = command.split()

        if len(command) > 1:
            cmd_args = command[1:]
        else:
            cmd_args = []

        command = command[0]

        if command == 'exit':
            self.exitScreen()

        elif command == 'connect':
            self.connectServer(cmd_args)

        elif command == 'disconnect':
            self.disconnectServer()

        else:
            # Forward command to server
            if self.connected_flag:
                self.client_net.sendMessage("\\"+command+" "+" ".join(cmd_args))
            else:
                self.addLine("Command not recognized by the client. Try connecting to a server first.")


    def entryBox(self):
        """ Handles entry box and input.
        """

        while 1:
            # Let the user edit until Ctrl-G is struck.
            self.box.edit()

            # Get resulting contents
            message = self.box.gather()

            # Do nothing when message box is empty
            if message == '':
                continue

            # Truncate message if too long
            if len(message) > self.text_width:
                message = message[0:self.text_width]


            # Clear previous input
            self.editwin.erase()

            # Detect if a commands is given
            if message[0] == '\\':
                self.handleCommands(message[1:].strip())
            else:
                if self.connected_flag:
                    self.client_net.sendMessage(message)
                else:
                    self.addLine("You are not connected to any server!\n")
                # Send message to output
                self.addLine(self.personal_prefix+message)


    def addLine(self, message):
        """ Adds a new line to the list of messages on the screen. 
        """

        # Remove extra newlines from both ends
        message = message.strip('\n')

        if '\n' in message:
            message = message.split('\n')
        else:
            message = [message]

        for line in message:
            self.message_lines.append(line)
            if len(self.message_lines) > self.message_row_size:
                self.message_lines.pop(0)

        self.showLines()
        

    def showLines(self):
        """ Shows lines from the list to the screen.
        """

        self.message_pad.erase()
        for row, line in enumerate(self.message_lines):
            self.message_pad.addstr(row, 0, line, curses.color_pair(1))

        self.message_pad.refresh(0, 0, self.mgs_lines_start, 0, self.message_row_size, self.text_width)

    def printWelcome(self):
        # Print a welcome message on the screen
        self.addLine('Welcome to the NerdTalk chat client!\nTo connect to a remote server write: \\connect IP port username\nTo exit write: \\exit\n')

    def exitScreen(self):
        """ Exit application.
        """
        # Set backend to disconnect
        self.disconnectServer()

        # Return terminal to normal state
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

        sys.exit(0)


if __name__ == "__main__":

    screen = curses.initscr()

    Screen(screen)