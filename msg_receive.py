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


# Receiver method is instantiated as its own separate thread away from the main process. This processes input
#     and figures out what to do with it! Be it a command that launches a /commands script, or just needs to print
#     it to screen and the log.
def receiver(connection):

    # Needed for later.
    partialmessage = ""

    # Create a commandpath navigation string to the commands folder, wherever we are. This is important for @reload and
    #     dynamic importing of the actual commands. This is stored inside the connection instance of IRCContext.
    connection.commandpath = os.path.join(connection.homedir, "commands")

    # Get a list of valid commands out of the loadCommands() function to check to make sure the command is appropriate.
    connection.valid_commands = utils.loadCommands(connection.commandpath)
    debug.echo(connection.debugmode, connection.valid_commands, "connection.valid_commands at top of receiver()")

    # Append commands folder path to the PYTHONPATH
    sys.path.append(connection.commandpath)

    # Gotta loop around and around! Not gonna be receiving only one message, after all.
    while True:
        # Recieve up to 1kb of data from the socket!
        # Why 1kb? Why not. Better to go too large than too small, right?
        ircmsg = bytes.decode(connection.ircsock.recv(1024))

        # Depending on quiet/headless mode we want to print to the screen if applicable. (quiet != true)
        if connection.quiet_mode == True:
            pass
        else:
            print(ircmsg)

        while True:
            ircmsg = partialmessage + ircmsg
            partition = ircmsg.partition("\r\n")
            debug.echo(connection.debugmode, str(partition), "msg partition")
            if partition[1] == "":
                partialmessage = partition[0]
                break
            else:
                # Call utils.getMsgClass() to instantiate the class of the message. See utils.py for more on this.
                msgclass = utils.getMsgClass(partition[0])

                # If it returns None (msg not recognized and/or we don't care about what it is) pass and
                #     loop around to top.
                if msgclass is None:
                    pass

                # Otherwise, (we know what the command is and it has a class instantiation) we check the class
                #     instances' 'isCommand' variable. If true, we execute its do() function and pass in the
                #     connection class instance of contexts.IRCContext
                else:

                    for queued_item in connection.processQ:

                        # If not empty, see if the item we've received matches what is being waited for on the Q
                        if msgclass.name in queued_item.activate_on:

                            # If it matches up with what we're waiting for, run the run() therein!
                            queued_item.run(connection, msgclass)
                        else:
                            pass

                    # "filters" through the list and removes anything that is finished, returning a cleaned list
                    connection.processQ = list(filter((lambda x: not x.finished), connection.processQ))



                    if msgclass.isCommand == True:
                        try:
                            msgclass.do(connection)
                        except OSError:
                            sys.exit()
                    else:
                        pass
                if partition[2] == "" and partialmessage != "":
                    partialmessage = ""
                else:
                    ircmsg = partition[2]