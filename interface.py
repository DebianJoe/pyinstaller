#!/usr/bin/env python

import curses
import os


# Gotta be root to get stuff done. (uncomment when ready for implementation)
# most of the execute calls need root anyhow (fdisk, parted, etc.)
if os.geteuid() != 0:
     print "You need to have root privileges to use this script."
     exit("Please try again, this time using 'sudo'. Exiting.")


# Set GLOBAL curses functions
screen = curses.initscr()

# Set GLOBAL Variables for actual install setup.
GRUB_DEV = None     # Where are we going to install Grub?
BOOT_DEV = None     # Where is the physical location of Boot?
FS_TYPE_BOOT = None # What Filesystem Type for Boot?
INSTALL_DEV = None  # Where is the main install going?
FS_TYPE_OS = None   # What Filesystem Type is main install?

# The basic order of things should be::
# 1. Partition, offer cfdisk (or carry on)
# 2. See if user wants to use /boot.  Give fdisk -l AND blkid as options
# 3. Get location for main install. Give fdisk -l AND blkid as options.
# 4. Get drive for grub (or carry on)


# an input string handling function
def get_param(prompt_string, extra):
     screen.clear()
     screen.border(1)
     screen.addstr(2, 2, prompt_string)
     if extra != None:
          screen.addstr(3, 3, extra)
     screen.refresh()
     input = screen.getstr(10, 10, 60)
     return input

# function for clean calls to os.system
def execute_cmd(cmd_string):
     os.system("clear")
     a = os.system(cmd_string)
     print ""
     if a == 0:
          print "Command executed correctly"
     else:
          curses.endwin()
          print "Command terminated with error"
     raw_input("Press enter")
     print ""

# Starting loop.
def opening():
     x = 0 # x is our choice for step #
     while x != ord('2'):
          screen.clear()
          screen.border(0)
          screen.addstr(0, 0, "Setup Partition Table")
          screen.addstr(2, 2, "Please enter a number...")
          screen.addstr(4, 4, "1 - Set up partition with parted")
          screen.addstr(5, 4, "2 - I have a partition prepared")
          screen.refresh()
          x = screen.getch()

          if x == ord('1'):
               execute_cmd("parted")
               curses.endwin()
     curses.endwin()

def choose_filesystem(partition):
     x = 0
     while x != ord('5'):
          screen.clear()
          screen.border(1)
          screen.addstr(0, 0, "Choose Filesytem for")
          screen.addstr(1, 0, partition)
          screen.addstr(2, 2, "Please enter a number...")
          screen.addstr(4, 4, "1 - ext2")
          screen.addstr(5, 4, "2 - ext2")
          screen.addstr(6, 4, "3 - ext3")
          screen.addstr(7, 4, "4 - btrfs")
          screen.refresh()
          x = screen.getch()
          curses.endwin()

          if x == ord('1'):
               return "btrfs"
          if x == ord('2'):
               return "ext2"
          if x == ord('3'):
               return "ext3"
          if x == ord('4'):
               return "ext4"

def boot_setup():
     ''' TODO, get Filesystem for /boot if it is being used.'''
     global BOOT_DEV, FS_TYPE_BOOT
     x = 0 # x is our choice
     while x != ord('4'):
          screen.clear()
          screen.border(0)
          screen.addstr(0, 0, "Setup /boot partition")
          screen.addstr(2, 2, "Please enter a number...")
          screen.addstr(4, 4, "1 - Specify a /boot partition")
          screen.addstr(5, 4, "2 - Use fdisk -l to list partitions")
          screen.addstr(6, 4, "3 - Use 'blkid -o list' to check partitions.")
          screen.addstr(7, 4, "4 - Done, or no /boot used.")
          screen.refresh()
          if BOOT_DEV != None:
               screen.addstr(8, 6, ("/boot location at %s" % BOOT_DEV))
          if FS_TYPE_BOOT != None:
               screen.addstr(9, 6, ("will be formatted to %s" % FS_TYPE_BOOT))
          screen.refresh()

          x = screen.getch()

          if x == ord('1'):
               # do we even want a special boot device?
               BOOT_DEV = get_param("Enter Partition name for /boot", None)
               FS_TYPE_BOOT = choose_filesystem("boot")
               curses.endwin()
          if x == ord('2'):
               screen.clear()
               curses.endwin()
               execute_cmd("fdisk -l")
               curses.endwin()
          if x == ord('3'):
               curses.endwin()
               execute_cmd("blkid -o list")
               curses.endwin()
     curses.endwin()

if __name__ == "__main__":
     # flow control for each function #
     opening()
     boot_setup()
     curses.endwin()
