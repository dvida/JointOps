import curses
from curses.textpad import Textbox, rectangle

class Screen():
    def __init__(self, stdscr, host_name):
        self.timer = 0
        self.host_name = "NerdTalk - connected to: "+host_name
        self.stdscr = stdscr

        # set screen attributes
        self.stdscr.nodelay(1) # this is used to make input calls non-blocking
        #curses.cbreak()
        #self.stdscr.keypad(1)
        #curses.curs_set(0)     # no annoying mouse cursor

        curses.noecho()
        curses.curs_set(1) # 1 - show cursor, 0 - hide cursor
        screen.keypad(1)

        self.rows, self.cols = self.stdscr.getmaxyx()
        self.message_lines = []

        curses.start_color()
        #curses.use_default_colors()
        # Create new pair with No. 1, with colors 8 and 0
        curses.init_pair(1, 6, 0)

        # Init entry box

        bottom_line = self.rows - 1

        text_heigth = 1
        self.text_width = self.cols-3
        text_top = bottom_line - text_heigth - 3
        text_left = 1

        self.editwin = curses.newwin(text_heigth,self.text_width, text_top,text_left)

        rectangle_top = text_top - 1
        rectangle_left = text_left - 1
        rectangle_bottom = rectangle_top + text_heigth + 2
        rectangle_right = rectangle_left + self.text_width + 2

        # Determine maximum lines visible on the message pad before shifting
        self.mgs_lines_start = 1
        self.msg_lines_end = rectangle_top - 1
        self.message_row_size = self.msg_lines_end - self.mgs_lines_start

        rectangle(self.stdscr, rectangle_top,rectangle_left, rectangle_bottom, rectangle_right)

        self.box = Textbox(self.editwin)

        # Write host on the top of the screen
        host_center = (self.cols-1)/2 - len(self.host_name)/2 - 1
        self.stdscr.addstr(0, host_center, self.host_name, curses.color_pair(1))

        self.stdscr.refresh()

        # Init message pad
        self.message_pad = curses.newpad(self.msg_lines_end - self.mgs_lines_start, self.text_width)
        #self.message_pad.refresh(0, 0, 5, 5, 10, 60)
        self.message_pad.refresh(0, 0, self.mgs_lines_start, 0, self.message_row_size, self.text_width)

        # Start entry box
        self.entryBox()

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

            # Clear preivous input
            self.editwin.erase()

            # Send message to output
            self.addLine(message)

            self.showLines()

            #self.stdscr.addstr(0, 0, message, curses.color_pair(1))
            #self.stdscr.refresh()

    def addLine(self, message):
        """ Adds a new line to the list of messages on the screen. 
        """
        self.message_lines.append(message)
        if len(self.message_lines) > self.message_row_size:
            self.message_lines.pop(0)
        

    def showLines(self):
        """ Shows lines from the list to the screen.
        """
        #self.stdscr.erase()
        self.message_pad.erase()
        for row, line in enumerate(self.message_lines):
            self.message_pad.addstr(row, 0, line, curses.color_pair(1))

        #self.stdscr.refresh()
        self.message_pad.refresh(0, 0, self.mgs_lines_start, 0, self.message_row_size, self.text_width)


# def main(stdscr):
#     #stdscr.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")

#       # Init entry box

#     bottom_line = curses.LINES - 1

#     text_heigth = 1
#     text_width = curses.COLS-3
#     text_top = bottom_line - text_heigth - 5
#     text_left = 1

#     editwin = curses.newwin(text_heigth,text_width, text_top,text_left)

#     rectangle_top = text_top - 1
#     rectangle_left = text_left - 1
#     rectangle_bottom = rectangle_top + text_heigth + 2
#     rectangle_right = rectangle_left + text_width + 2

#     rectangle(stdscr, rectangle_top,rectangle_left, rectangle_bottom, rectangle_right)

#     box = Textbox(editwin)

#     stdscr.refresh()

#     while 1:

#       # Let the user edit until Ctrl-G is struck.
#       box.edit()

#       # Get resulting contents
#       message = box.gather()

#       # Clear preivous input
#       editwin.erase()

#       # Send message to output
#       stdscr.addstr(0, 0, message)

#       stdscr.refresh()


screen = curses.initscr()
#curses.noecho()
#curses.curs_set(1)
#screen.keypad(1)

Screen(screen, 'LOCALHOST')
#main(screen)