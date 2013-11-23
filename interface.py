#!/usr/bin/env python

import curses
import os
import subprocess

# Gotta be root to get stuff done.  Testing as root because
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
NEW_HOSTNAME = "bbq"# The name that the user would like.

# The basic order of things should be::
# 1. Partition, offer cfdisk (or carry on)
# 2. See if user wants to use /boot.  Give fdisk -l AND blkid as options
# 3. Get location for main install. Give fdisk -l AND blkid as options.
# 4. Get drive for grub (or carry on)
# 5. Prompt User for new hostname
# 6. Provide Summary before committing changes to disk.



######## User Interface Functions ###############

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
          screen.addstr(4, 4, "1 - btrfs")
          screen.addstr(5, 4, "2 - ext2")
          screen.addstr(6, 4, "3 - ext3")
          screen.addstr(7, 4, "4 - ext4")
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
               screen.addstr(10, 6, "press 4 if you're happy with that")
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

def main_setup():
     global FS_TYPE_OS, INSTALL_DEV
     x = 0 # x is our choice
     while x != ord('4'):
          screen.clear()
          screen.border(0)
          screen.addstr(0, 0, "Setup /root partition")
          screen.addstr(2, 2, "Please enter a number...")
          screen.addstr(4, 4, "1 - Specify a /root partition")
          screen.addstr(5, 4, "2 - Use fdisk -l to list partitions")
          screen.addstr(6, 4, "3 - Use 'blkid -o list' to check partitions.")
          screen.addstr(7, 4, "4 - Done")
          screen.refresh()
          if INSTALL_DEV != None:
               screen.addstr(9, 6, ("/ location at %s" % INSTALL_DEV))
          if FS_TYPE_OS != None:
               screen.addstr(10, 6, ("will be formatted to %s" % FS_TYPE_OS))
               screen.addstr(11, 6, "press 4 if you're happy with that.")
          screen.refresh()

          x = screen.getch()

          if x == ord('1'):
               # required section.
               INSTALL_DEV = get_param("Enter Partition name for /root", None)
               FS_TYPE_OS = choose_filesystem(" / ")
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

def grub_setup():
     global GRUB_DEV
     x = 0 # x is our choice
     while x != ord('2'):
          screen.clear()
          screen.border(0)
          screen.addstr(0, 0, "Grub Setup")
          screen.addstr(2, 2, "Please enter a number...")
          screen.addstr(4, 4, "1 - Specify a device for GRUB")
          screen.addstr(5, 4, "2 - Done")
          screen.addstr(7, 2, \
                    "Leave blank if you don't wish to install a bootloader.")
          screen.refresh()
          if GRUB_DEV != None:
               screen.addstr(9, 6, ("GRUB location at %s" % GRUB_DEV))
          screen.refresh()

          x = screen.getch()

          if x == ord('1'):
               # IF grub is needed
               GRUB_DEV = get_param("Enter device name for GRUB", \
                                    "Usually a drive, like /dev/sda")
               curses.endwin()
     curses.endwin()

def hostname_setup():
     global NEW_HOSTNAME
     x = 0 # x is our choice
     while x != ord('2'):
          screen.clear()
          screen.border(0)
          screen.addstr(0, 0, "Hostname")
          screen.addstr(2, 2, "Would you like to change the hostname?")
          screen.addstr(4, 4, "1 - Yes")
          screen.addstr(5, 4, "2 - No")
          screen.refresh()
          x = screen.getch()

          if x == ord('1'):
               NEW_HOSTNAME = get_param("Enter your desired hostname", None)
               x = ord('2')

     curses.endwin()

def summary():
     global NEW_HOSTNAME, BOOT_DEV, FS_TYPE_BOOT, INSTALL_DEV, FS_TYPE_OS, \
     GRUB_DEV, NEW_HOSTNAME
     x = 0 # x is our choice
     while x != ord('2'):
          screen.clear()
          screen.border(0)
          screen.addstr(0, 0, "Summmary!")
          if BOOT_DEV != None:
               screen.addstr(2, 2, ("/boot located at %s" % BOOT_DEV))
               screen.addstr(3, 3, ("and formatted as %s" % FS_TYPE_BOOT))
          elif BOOT_DEV == None:
               screen.addstr(2, 2, "no /boot partition selected")
          screen.addstr(4, 2, ("/ located at %s" % INSTALL_DEV))
          screen.addstr(5, 3, ("and formatted as %s" % FS_TYPE_OS))
          if GRUB_DEV != None:
               screen.addstr(6, 2, ("GRUB to be installed to %s" % GRUB_DEV))
          elif GRUB_DEV == None:
               screen.addstr(6, 2, "a bootloaded will not be installed")
          if NEW_HOSTNAME != None:
               screen.addstr(7, 2, ("Hostname will be %s" % NEW_HOSTNAME))
          screen.addstr(9, 4, "Press '2' to commit changes to drive.")
          screen.addstr(10, 4, "or press 0 to exit installer.")
          screen.refresh()
          x = screen.getch()
          if x == ord('0'):
               exit_cleanly("User has cancelled install at summary")
     curses.endwin()

###### Non-user seen functions #########

def do_run_in_chroot(command):
     #because we need to be able to call it as a function
     os.system("chroot /target/ /bin/sh -c \"%s\"" % command)

def do_mount(options, fstype, device, dest):
     # the 'fstype' is the filesystem type, device is what to mount #
     # and 'dest is where the device is to be mounted.            #
     if(options is not None):
          cmd = "mount -o %s -t %s %s %s" % \
                (options, fstype, device, dest)

def do_Umount(options, fstype, device, dest):
     if(options is not None):
          cmd = "mount -o %s -t %s %s %s" % \
                (options, fstype, device, dest)

def create_fs(filesystem, device):
     if(filesystem is not None):
          cmd = "mke2fs -t %s %s" % \
                (filesystem, device)
          tune = "tune2fs -r 1000 %s" % device
          os.system(cmd)

def exit_cleanly(reason):
     curses.endwin()
     print "\033[2J\033[1;H"
     print "%s\n" % reason
     exit(1)

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
# designed to PAUSE, so NOT for linear calls
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

def installer_engine():
     # The Sequencer for the install process.
     global NEW_HOSTNAME, BOOT_DEV, FS_TYPE_BOOT, INSTALL_DEV, FS_TYPE_OS, \
     GRUB_DEV, NEW_HOSTNAME
     os.system("mkdir /target")
     create_fs(FS_TYPE_OS, INSTALL_DEV)
     # mount INSTALL_DEV on /target

###################################################

####### Main Program ##############################

if __name__ == "__main__":
     # flow control for each function #
     opening()
     boot_setup()
     main_setup()
     grub_setup()
     hostname_setup()
     summary()
     curses.endwin()

     # This added for debug purposes.
