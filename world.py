# This is the world file, where most of the functions are going to be defined.

# Importing os for changing working directories.
# Importing sys for appending to pythonpath.
import os
import sys

# Global variable definitions!
# ValidChars goes over the stuff that is going to be accepted by anything that eventually gets passed to SQL
validchars = "abcdefghijklmnopqrstuvwxyz#@"

# Before we do anything, however, we have to have a list of commands we are looking for.
# This is loaded from the commands folder. We then grab a list of the files therein, replace the ".py" extensions, and
#     then append them to a list of valid commands. Then we reclaim the massive memory expenditure of tempdirlist.
# Because I can't get lists to return properly for whatever reason, we are going to edit the global variable
#     valid_commands because it works and I am thrice damned to figure out why returning doesn't.
def loadValidModules():
    valid_commands = []
    if "commands" in os.getcwd():
        tempdirlist = os.listdir()
        for x in tempdirlist:
            valid_commands.append(x.replace(".py", ""))
        print("Valid commands for this instance are " + str(valid_commands))
        tempdirlist = None
        return valid_commands
    else:
        try:
            os.chdir("commands")
        except FileNotFoundError:
            print(" FileNotFoundError, breaking. Check what the hell your environ looks like.")
            return None
        curpath = os.getcwd()
        sys.path.append(curpath)
        return loadValidModules()

# This function finds out what the channel is in ircmsg.
# It finds the first # and then grabs all the text after that until the next space if there is one,
# if not, it goes until end of message.
# Let's say IRC message equals Hekter~@34jkl34hklj4.bhjkr.com :@join #HekterBot
# chanstart will equal the location of #
# Then stating there, it will grab the location of the next space after the #
# If there is no space after the # sign, chan will equal the rest of the string, in this case, #HekterBot
def changrab(ircmsg):
    print("ircmsg inside changrab isssss " + str(ircmsg))
    chanstart = ircmsg.find("#")
    print("chanstart isss " + str(chanstart))
    if chanstart == -1:
        return None
    else:
        pass
    chanend = ircmsg[chanstart:].find(" ")
    print("chanend isss " + str(chanend))
    if chanend > -1:
        chan = ircmsg[chanstart:(chanend + chanstart)]
    else:
        chan = ircmsg[chanstart:]
        print("chan issss " + str(chan))

    # Checks to make sure all the parsed chan characters are valid and eliminates the chance of an SQL injection
    #     as well as reducing the amount of invalid channels getting appended to the database.
    for character in chan:
        print("character issss " + str(character))
        if character not in validchars:
            return None
        else:
            pass
    return chan

# Used for sending messages to a channel!
def sendmsg(ircsock, chan, msg):
    try:
        ircsock.send(str.encode("PRIVMSG " + chan + " " + msg + "\r\n"))
    except OSError:
        print("Oh lawd, ship's goin' down, son!")
        sys.exit()

# Used to actually join channels.
def joinchan(ircsock, chan, pw):

    # If the password returns "None", set to an empty string.
    if pw == "None":
        pw = ''
    else:
        pass
    try:
        ircsock.send(str.encode("JOIN " + chan + pw))
    except OSError:
        print("Sweet Jesus! Mayday! Mayday!")
        sys.exit()

# This is receiver, which gets instantiated as its own separate thread in inumuta.py.
# It gets passed ircsock which is the socket connection to the IRC server. This is so it can receive messages on the
#    socket.
def receiver(ircsock):
    # Use loadValidModules() to get a list of valid commands in /commands
    valid_commands = loadValidModules()
    # print(str(commandlist) + " commandlist at top of receiver()")
    print(str(valid_commands) + " valid_commands at top of receiver()")
    # Reciever() entirely takes place inside an infinite loop so that is continually receiving messages from the server.
    while True:

        # ircmsg = received data (up to 2kb) on the socket. Arbitrary limit. IRC does not output more than 255 chars.
        # bytes.decode used to make the data into usable regular strings as opposed to bloody bytecode.
        # It also strips all the newlines and return carriages since those are sent along with the message.
        # Put ircmsg into lower case to help with validity checks
        ircmsg = bytes.decode(ircsock.recv(2048)).strip('\n\r').lower()

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
            # ---:(ircmsg[command_start + 2:].find(" ") + 2 + command_start)]
            # This gets the final entry in the string splice by starting where the command string begins, and ending
            #     where it hits the first space. It adds 2 because the command string it's looking for is 2 long (:@)
            #     and adds command_start because it's still parsing ircmsg and the .find(" ") only gives the local
            #     "spaces from command_start" value and needs to be added on to get the real coordinate.
            # Spaceless variant works the same way, but just the first step without all the extra space shenanigans.
            if space:
                command = ircmsg[(command_start + 2):((ircmsg[(command_start + 2):].find(" ")) + 2 + command_start)]
                print(str(command) + " command with spaces")
            else:
                command = ircmsg[(command_start + 2):]
                print(str(command) + " command without spaces")

            # Now we figure out if the command we grabbed is even valid.
            # If it is, import that command
            # If it returns "broken", assume everything is broken forever and panic.
            if command in valid_commands:
                runcommand = __import__(command)
                print(str(runcommand))
                returnedVar = runcommand.run(ircsock, ircmsg)
                if returnedVar == "broken":
                    print("Everything is broken forever.")
                    sys.exit()
                else:
                    pass

            # # Creating a special rule to *reload valid commands/modules* outside of the /commands folder
            elif command == "reload":
                valid_commands = loadValidModules()

            # Otherwise, send invalid command message.
            else:
                chan = changrab(ircmsg)
                if chan == None:
                    pass
                # THIS NEEDS TO BE EXAMINED LATER
                sendmsg(ircsock, chan, " :Invalid command!\r\n")

        # Compliance with IRC standards--PING/PONG response.
        elif ircmsg.find("ping :") > -1:
            ircsock.send(str.encode("PONG " + ircmsg[5:] + "\r\n"))

        # If nothing to be found, return to top of the loop.
        else:
            pass