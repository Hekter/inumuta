# This is the world file, where most of the functions are going to be defined.

# Importing os for changing working directories.
# Importing sys for appending to pythonpath.
import os
import sys

# Testing this shit with global variables because why not.
valid_commands = []

# Before we do anything, however, we have to have a list of commands we are looking for.
# This is loaded from the commands folder. We then grab a list of the files therein, strip the ".py" extensions, and
#     then append them to a list of valid commands. Then we reclaim the massive memory expenditure of tempdirlist.
def loadValidModules():
    global valid_commands
    valid_commands = []
    if "commands" in os.getcwd():
        tempdirlist = os.listdir()
        for x in tempdirlist:
            valid_commands.append(x.strip(".py"))
        print("Valid commands for this instance are " + str(valid_commands))
        # tempdirlist = None
        # return valid_commands
        return
    else:
        try:
            os.chdir("commands")
        except FileNotFoundError:
            print(" FileNotFoundError, breaking. Check what the hell your environ looks like.")
            return None
        curpath = os.getcwd()
        sys.path.append(curpath)
        loadValidModules()

# This is receiver, which gets instantiated as its own separate thread in inumuta.py.
# It gets passed ircsock which is the socket connection to the IRC server. This is so it can receive messages on the
#    socket.
def receiver(ircsock):
    # Use loadValidModules() to get a list of valid commands in /commands
    # commandlist = loadValidModules()
    loadValidModules()
    print(str(valid_commands) + " valid_commands at top of receiver()")
    # Reciever() entirely takes place inside an infinite loop so that is continually receiving messages from the server.
    while True:

        # ircmsg = received data (up to 2kb) on the socket. Arbitrary limit. IRC does not output more than 255 chars.
        # bytes.decode used to make the data into usable regular strings as opposed to bloody bytecode.
        # It also strips all the newlines and return carriages since those are sent along with the message.
        ircmsg = bytes.decode(ircsock.recv(2048)).strip('\n\r')

        # No matter what we want to see what we receive!
        print(ircmsg)

        # Next we find out if the line received actually contains a command. It finds the location of :@ which will
        #     at the beginning of the sent line by the server if a command is present.
        command_start = ircmsg.find(":@")
        # print(str(command_start) + " command_start coordinate")

        # If the command symbol is present, grab the command (word after the :@) and check to see if it's
        #     located inside valid_commands. Then grab the string of text between :@ and the first space.
        if command_start > -1:

            # First check to see if there are any spaces we need to account for after the (presumed) command.
            # Set boolean appropriately.
            if ircmsg[(command_start + 2):].find(" ") > -1:
                space = True
            else:
                space = False

            # Now grab the command based on whether or not there are spaces. Grabbing command works as follows:
            # ircmsg[(command_start) + 2)---
            # This starts reading the string at the location where the command string (:@) begins, plus 2 because
            #     that is the length of the command string
            # ---:(ircmsg[command_start + 2:].find(" ") + 1)]
            # This gets the final entry in the string splice by starting where the command string begins, and ending
            #     where it hits the first space.
            # Spaceless variant works the same way, but just the first step without all the extra space shenanigans.
            if space:
                command = ircmsg[(command_start + 2):(ircmsg[(command_start + 2):].find(" "))]
                print(str(command) + " command with spaces")
            else:
                command = ircmsg[(command_start + 2):]
                print(str(command) + " command without spaces")

            # Now we figure out if the command we grabbed is even valid.
            # If it is, import that command
            if command in valid_commands:
                runcommand = __import__(command)
                print(str(runcommand))
                runcommand.run(ircsock, ircmsg)

            # Creating a special rule to *reload valid commands/modules* outside of the /commands folder
            elif command == "reload":
                # commandlist = loadValidModules()
                loadValidModules()

            # Otherwise, send invalid command message.
            else:
                chan = changrab(ircmsg)
                ircsock.send(str.encode("PRIVMSG " + chan + " :Invalid command!\r\n"))

        # Compliance with IRC standards--PING/PONG response.
        elif ircmsg.find("PING :") > -1:
            ircsock.send(str.encode("PONG " + ircmsg[5:] + "\r\n"))

        # If nothing to be found, return to top of the loop.
        else:
            pass

def changrab(ircmsg):
    chanstart = ircmsg.find("#")
    chan = ircmsg[chanstart:(ircmsg[chanstart:].find(" ") + chanstart)]
    return chan