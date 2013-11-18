#!/usr/bin/env python

import curses
import os
x = 0

# an input string handling function
def get_param(prompt_string):
     screen.clear()
     screen.border(0)
     screen.addstr(2, 2, prompt_string)
     screen.refresh()
     input = screen.getstr(10, 10, 60)
     return input


def execute_cmd(cmd_string):
     os.system("clear")
     a = os.system(cmd_string)
     print ""
     if a == 0:
          print "Command executed correctly"
     else:
          print "Command terminated with error"
     raw_input("Press enter")
     print ""

# Main loop.

while x != ord('4'):
    screen = curses.initscr()

    screen.clear()
    screen.border(0)
    screen.addstr(2, 2, "Please enter a number...")
    screen.addstr(4, 4, "1 - Add some fields")
    screen.addstr(5, 4, "2 - Selection 2")
    screen.addstr(6, 4, "3 - Show disk space")
    screen.addstr(7, 4, "4 - Exit")
    screen.refresh()

    x = screen.getch()

    if x == ord('1'):
        username = get_param("Enter the username")
        homedir = get_param("Enter the home directory, eg /home/nate")
        groups = get_param("Enter comma-separated groups, eg adm,dialout,cdrom")
        shell = get_param("Enter the shell, eg /bin/bash:")
        screen.addstr(2, 2, username)
        curses.endwin()
    if x == ord('2'):
        curses.endwin()
    if x == ord('3'):
        curses.endwin()
        execute_cmd("df -h")

curses.endwin()
