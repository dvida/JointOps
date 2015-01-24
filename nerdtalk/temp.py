#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
import curses.textpad

screen = curses.initscr()
curses.noecho()
curses.curs_set(0)
screen.keypad(1)


bottom_pos = curses.LINES - 1 
left_pos = 0
screen.addstr(bottom_pos, left_pos, "Positioned String")
#screen.addstr(bottom_pos, left_pos, "Positioned String2")
#screen.addstr("Positioned String")




pad = curses.newpad(100, 100)
# These loops fill the pad with letters; addch() is
# explained in the next section
for y in range(0, 99):
    for x in range(0, 99):
        pad.addch(y,x, ord('a') + (x*x+y*y) % 26)

pad.refresh( 0,0, 5,5, 20,75)




while True:
   event = screen.getch()
   if event == ord("q"): break
   
curses.endwin()

#!/usr/bin/env python
 

 

 
#hw = "Hello world!"
#while 1:
# c = stdscr.getch()
# if c == ord('p'):
# elif c == ord('q'): break # Exit the while()
# elif c == curses.KEY_HOME: x = y = 0
