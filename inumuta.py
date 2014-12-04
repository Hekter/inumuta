# This is Inumuta, a basic IRC bot that offers Sovereign-like functions that can be added / removed at will.
# I'm going to be following heavy documentation during this project in order to make it a) more understandable by others
# and b) more understandable by me when I have to go back and look at this six months from now and try to figure out
#     what the hell I was thinking at the time.
# Of course, Python doesn't do multi-line comments, so this will be extra fun.

# Since this is an IRC client, we need some basic imports.
# Socket for ... sockets
# time for sleeping
# threading for non-concurrent processing (sending and receiving messages)
# sys for various things like exit
# os for changing interacting with directories
import socket
import time
import threading
import sys
import os

# Now for custom imports.
# world is the location of all the regular program-wide functions including changrab() and receiver()
# commands.join for joining the default channel
import world
import commands.join as join

# One of these days this will load from a config file, but for the moment we're going to set some global variables.
# SERVER = IRC server connecting to.
# DEFAULTCHANNEL = First room to connect to--essentially a default option. This is to make sure the bot is working and to
#     issuing other commands.
# BOTNICK = The bot's nick. What it will be named on the IRC network. By default "Inumuta"
# PASSWORD = Password to identify the nick with Nickserv, available on most IRC networks.
# chanlist =  Empty list to store currently-connected channels.
# threads = Empty list to store the list of current threads
SERVER = "irc.rizon.net"
DEFAULTCHANNEL = "#HekterBot"
BOTNICK = "Inumuta"
PASSWORD = "pancakes"
chanlist = []
threads = []

#Now we need to establish whether or not the database exists.
cwdFileList = os.listdir()
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
t = threading.Thread(target=world.receiver, args=(ircsock,))
threads.append(t)
t.start()

# IRC protocol dicatates we have to identify ourselves with username nonsense.
# We sleep for two seconds to let the IRC server catch up to us, otherwise we move too fast and stuff gets lost.
ircsock.send(str.encode("USER " + BOTNICK + " " + BOTNICK + " " + BOTNICK + " :" + BOTNICK + "\r\n"))
time.sleep(2)

# Next IRC protocol says we need to establish a nickname.
ircsock.send(str.encode("NICK " + BOTNICK + "\r\n"))
time.sleep(2)

# Then we send along the nickserv password to get our permissions and to be identified.
ircsock.send(str.encode("NickServ IDENTIFY " + PASSWORD + "\r\n"))
time.sleep(2)

# Then we join the default channel.
join.run(ircsock, DEFAULTCHANNEL)
# ircsock.send(str.encode("JOIN " + DEFAULTCHANNEL + "\r\n"))

# The program continues to run inside the receiver() function located in world.