# World file! Because if there's anything I want to be known for when this is all over, it's that I name my modules
#     very weirdly.

# Import os for directory shenanigans!
import os
# Import sys for pythonpath manipulation! Also, exiting.
import sys

# Custom imports!
# Debugtools, yay!
import debugtools as debug

DEBUGMODE = debug.prompt()

# Let's define some global variables because reasons.
# VALIDCHARS is.. well.. valid characters. Don't want any of those special characters mucking up the DB or somesuch.
VALIDCHARS = "abcdefghijklmnopqrstuvwxyz#@ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Before we do anything, however, we have to have a list of commands we are looking for.
# This is loaded from the commands folder. We then grab a list of the files therein, replace the ".py" extensions, and
#     then append them to a list of valid commands.
# Homedir is wherever the script is located. This is the basis for getting into commands/ without changing CWD.
def loadCommands(commandpath):

    # Empty commands list to store commands as they get appended in.
    commands = []

    # [Temporarily] grab the list of crap inside commands
    try:
        tempdirlist = os.listdir(commandpath)
    except FileNotFoundError:
        print("Commands folder not found. Check filesystem and install documentation.")
        sys.exit()

    # Iterate over the items inside dirlist and append them to commands
    for x in tempdirlist:
        if x == "__init__.py" or x == "__pycache__":
            pass
        else:
            commands.append(x.replace(".py", ""))
    debug.echo(DEBUGMODE, commands, "commands")
    return commands

# Used for sending messages to a channel!
def sendmsg(ircsock, chan, msg):
    try:
        ircsock.send(str.encode("PRIVMSG " + chan + " :" + msg + "\r\n"))
    except OSError:
        print("Oh lawd, ship's goin' down, son!")
        sys.exit()

# Used for sending IRC-codified message to join a channel.
def joinChan(ircsock, chan, pw):
    try:
        ircsock.send(str.encode("JOIN " + chan + " " + pw + "\r\n"))
    except OSError:
        print("Mother of Arceus.")
        sys.exit()

def argGrabber(msg, position):
    # Attempt to grab the argument. If there is no argument (IndexError), set to blank string
    try:
        arg = msg[position]
        return arg
    except IndexError:
        arg = ''
        return arg

# This is receiver, which is actually instantiated as a thread inside inumuta.py to run seperately from the main process
# In it gets passed ircsock with the open socket used to connect to the server, and homedir which is a path to where
#     the inumuta install is located.
def receiver(ircsock, homedir, COMMANDCHAR):
    commandpath = os.path.join(homedir, "commands")
    # Use loadModules() to get the list of scripts available inside /commands
    # Also get the path to the commands folder
    commands = loadCommands(commandpath)
    print(str(commands) + " commands parsed.")
    sys.path.append(commandpath)

    # Now we need to load up the command character.

    # Receiver is a loop! Gotta keep receiving those messages.
    while True:
        # Recieve up to 2kb of data from the socket!
        ircmsg = bytes.decode(ircsock.recv(2048)).strip('\n\r')

        # No matter what we want to see what we receive!
        print(ircmsg)

        # Split the received message into a list.
        ircmsg = ircmsg.split()

        # Part of IRC authentication and connection-monitoring, PINGs must be responded to with PONGs
        if ircmsg[0] == "PING":
            ircsock.send(str.encode("PONG " + ircmsg[1] + "\r\n"))
            print("PONG " + ircmsg[1])

        # If the commandchar is in thar, load it up, yo :D
        try:
            # comflag = ircmsg[3]
            if COMMANDCHAR in ircmsg[3]:

                # Set command var to ircmsg[3][2:] to cutt off the first two characters (colon and commandchar)
                command = ircmsg[3][2:]

                # Check to make sure the command is even in the valid command list for import!
                if command in commands:
                    # Set runcommand to the import of whatever module we've just loaded with the name equalling the command.
                    runcommand = __import__(command)

                    # Now invoke that module's run() function and grab whatever it spits back out.
                    returnedVar = runcommand.run(ircsock, ircmsg, homedir)

                    # Check to see if the returned variable is the string "broken" which indicates something has gone
                    #     horribly, horribly wrong and the bot needs to shut down now.
                    if returnedVar == "broken":
                        print("Everything is broken forever.")
                        sys.exit()
                    elif returnedVar == "invalidArg":
                        chan = ircmsg[2]
                        sendmsg(ircsock, chan, "Invalid argument! Check for invalid characters or formatting.\r\n")
                    else:
                        pass

                # Now we have some custom, special commands reserved for administrative use.
                elif command == "reload":
                    commands = loadCommands(commandpath)
                elif command == "debug-on":
                    global DEBUGMODE
                    DEBUGMODE = True
                elif command == "debug-off":
                    global DEBUGMODE
                    DEBUGMODE = False

                # And if all else fails, we have a command char with an invalid command! We should say something.
                else:
                    chan = ircmsg[2]
                    sendmsg(ircsock, chan, "Invalid command!\r\n")
        except:
            pass