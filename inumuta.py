# This is Inumuta, a basic IRC bot that offers Sovereign-like functions that can be added / removed at will.
# I'm going to be following heavy documentation during this project in order to make it a) more understandable by others
# and b) more understandable by me when I have to go back and look at this six months from now and try to figure out
#     what the hell I was thinking at the time.
# Of course, Python doesn't do multi-line comments, so this will be extra fun.

# Socket for ... sockets
import socket
# time for sleeping
import time
# threading for non-concurrent processing (sending and receiving messages)
import threading
# sys for various things like exit
import sys
# os for changing interacting with directories
import os
# sqlite3 as lite for sqlite, our database of choice
import sqlite3 as lite
# configparser to parse the glorious config file!
import configparser

# Now for custom imports.
# world is the location of all the regular program-wide functions like receiver()
import world
# utils for access to various classes :3
import formats
# debugtools for help with debugging!
import debugtools as debug

DEBUGMODE = debug.prompt()

# Instantiates ConfigParser() and loads settings.ini
settings = configparser.ConfigParser()
settings.read("settings.ini")

# TO BE REPLACED WITH SELECTION/INPUT/WHATEVER
settingsProfile = "DEFAULT"

# Loaded from settings.ini
# SERVER = IRC server connecting to.
# DEFAULTCHANNEL = First room to connect to--essentially a default option. This is to make sure the bot is working and
#     to issuing other commands.
# BOTNICK = The bot's nick. What it will be named on the IRC network. By default "Inumuta"
# PASSWORD = Password to identify the nick with Nickserv, available on most IRC networks.
# COMMANDCHAR = Special character at the start of an IRC line that indicates that it is a command.
SERVER = settings[settingsProfile]["SERVER"]
DEFAULTCHANNEL = settings[settingsProfile]["DEFAULTCHANNEL"]
DEFAULTCHANNELPW = settings[settingsProfile]["DEFAULTCHANNELPW"]
BOTNICK = settings[settingsProfile]["NICK"]
PASSWORD = settings[settingsProfile]["PASSWORD"]
COMMANDCHAR  = ":" + str(settings[settingsProfile]["COMMANDCHAR"])

# threads = Empty list to store the list of current threads.
# homedir = home directory where inumuta.py is located.
threads = []
homedir = str(os.getcwd())

#Now we need to establish whether or not the database exists.
cwdFileList = os.listdir(homedir)
if "inumuta.db" not in cwdFileList:
    import setup
    setup.run()
else:
    pass

# Now that we've established the beginning stuff, let's get down to actually doing things.
# First we need to actually make a socket, and then connect to server as defined in SERVER.
# We are using default port 6667 for the IRC protocol.
# In a try to make sure we can connect to server and create the socket. If not, exit program since there's no point
#     in running if we cannot connect to server.
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    ircsock.connect((SERVER, 6667))
except Exception as error:
    print("Unable to connect to server.")
    print(str(error))
    sys.exit()

# Now we are going to instantiate a thread to receive all messages and passing it the open socket.
# This utilizes the receiver() function inside the world import.
t = threading.Thread(target=world.receiver, args=(ircsock,homedir,COMMANDCHAR,))
threads.append(t)
t.start()

# IRC protocol dicatates we have to identify ourselves with username nonsense.
# We sleep for two seconds to let the IRC server catch up to us, otherwise we move too fast and stuff gets lost.
ircsock.send(str.encode("USER " + str(socket.gethostname()) + " 0 * :" + BOTNICK + "Bot\r\n"))
time.sleep(2)

# Next IRC protocol says we need to establish a nickname.
ircsock.send(str.encode("NICK " + BOTNICK + "\r\n"))
time.sleep(2)

# Skip this step if there is no password
if PASSWORD == '':
    pass
else:
    # Then we send along the nickserv password to get our permissions and to be identified.
    ircsock.send(str.encode("NickServ IDENTIFY " + PASSWORD + "\r\n"))
    time.sleep(2)

# Now we establish a connection to the database.
con = lite.connect(os.path.join(homedir, "inumuta.db"))
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM Chans")

    rows = cur.fetchall()

    if rows == []:
        world.joinChan(ircsock, DEFAULTCHANNEL, DEFAULTCHANNELPW)
    else:
        for row in rows:
            world.joinChan(ircsock, row[0], row[1])
            time.sleep(.5)


while True:
    # This allows us to be able to type into the console as it runs. We do need to specify which channel to talk to.
    # Format is #chanName :text
    uinput = input()
    ircsock.send(str.encode("PRIVMSG " + uinput + "\r\n"))

# The program continues to run inside the receiver() function located in world.
