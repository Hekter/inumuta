# Reinterpretation of world. Again. I think this makes this the third total re-write?

# Import os for directory shenanigans!
import os
# Import sys for pythonpath manipulation! Also, exiting.
import sys

# Custom imports!
# Debugtools, yay!
import debugtools as debug
# Utils for getMsgClass()
import utils

# Function looks at the contents of /commands folder and comes out with a list of valid commands therein. This is later
#     compared against user input to parse what is a valid command or not. This is accessed via the special @reload
#     command to "refresh" the list of valid commands while the bot is running.
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
    # We want to ignore __init__.py and __pycache__ since that's gonna make things... weird if we try to import them.
    for x in tempdirlist:
        if x == "__init__.py" or x == "__pycache__":
            pass
        else:
            commands.append(x.replace(".py", ""))
    print(str(commands))
    return commands

# Receiver method is instantiated as its own separate thread away from the main process. This processes input
#     and figures out what to do with it! Be it a command that launches a /commands script, or just needs to print
#     it to screen and the log.
def receiver(connection):

    # Create a commandpath navigation string to the commands folder, wherever we are. This is important for @reload and
    #     dynamic importing of the actual commands. This is stored inside the connection instance of IRCContext.
    connection.commandpath = os.path.join(connection.homedir, "commands")

    # Get a list of valid commands out of the loadCommands() function to check to make sure the command is appropriate.
    connection.valid_commands = loadCommands(connection.commandpath)
    debug.echo(connection.debugmode, connection.valid_commands, "connection.valid_commands at top of receiver()")

    # Append commands folder path to the PYTHONPATH
    sys.path.append(connection.commandpath)

    # Gotta loop around and around! Not gonna be receiving only one message, after all.
    while True:
        # Recieve up to 1kb of data from the socket!
        # Why 1kb? Why not. Better to go too large than too small, right?
        ircmsg = bytes.decode(connection.ircsock.recv(1024)).strip('\n\r')

        # No matter what we want to be printing what we receive to the screen.
        # FOR FUTURE: QUIET MODE
        print(ircmsg)

        # Now we take the message and convert it to a list. This list is the first two elements (hostname, command)
        #     and then the rest of the message. E.g.; 'pancakes are the tits, yo' becomes
        #     ['pancakes', 'are', 'the tits, yo']
        # 'None' separator specifies using a special algorithm to split on consecutive whitespace and to
        #     trim trailing space
        ircmsg = ircmsg.split(sep=None, maxsplit=2)

        # Call utils.getMsgClass() to instantiate the class of the message. See utils.py for more on this.
        msgclass = utils.getMsgClass(ircmsg)

        # If it returns None (msg not recognized and/or we don't care about what it is) pass and loop around to top.
        if msgclass is None:
            pass

        # Otherwise, (we know what the command is and it has a class instantiation) we check the class instances'
        #     'isCommand' variable. If true, we execute its do() function and pass in the connection class instance
        #     of contexts.IRCContext
        else:
            if msgclass.isCommand == True:
                msgclass.do(connection)
            else:
                pass