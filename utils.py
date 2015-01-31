import formats

import os

alphabet = "abcdefghijklmnopqrstuvwxyz"

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
    print("Valid commands: " + str(commands))
    return commands

def getMsgClass(msg):

    # Now we take the message and convert it to a list. This list is the first two elements (hostname, command)
    #     and then the rest of the message. E.g.; 'pancakes are the tits, yo' becomes
    #     ['pancakes', 'are', 'the tits, yo']
    # 'None' separator specifies using a special algorithm to split on consecutive whitespace and to
    #     trim trailing space
    msg = msg.split(sep=None, maxsplit=2)

    # Now we start a big ole if tree to find out if the message is a type we care about / can handle.
    # If so, we instantiate its class which contains how to do what it needs.
    if msg[1] == 'PRIVMSG':
        msgtype = formats.Privmsg(msg)
        return msgtype
    elif msg[0] == 'PING':
        msgtype = formats.Ping(msg)
        return msgtype
    elif msg[1] == '353':
        msgtype = formats.Code353(msg)
        return msgtype
    elif msg[1] == '366':
        msgtype = formats.Code366(msg)
        return msgtype
    else:
        return None

    # Now we make sure there aren't any invalid characters in our chan var :3
    # We set pound_count to 0 to ... count the # of #s :P We already established above we have at least 1, now to check
    #     and make sure there isn't any more than that.
def valid_chan(connection, privmsg, input_chan):

    # I should hope this is self-explanatory.
    if "#" not in input_chan:
        connection.send_msg(privmsg.chan, "Lacking a # to denote channame!")
        return False
    else:
        pass

    pound_count = 0
    for char in input_chan.lower():
        if char in alphabet:
            pass
        else:

            # If the invalid char (not-alphabet) is #, we go and make sure there's only one of them! This is done with
            #     incrementing the poundcount. If more than 1, return False and say there's too damn many of the things.
            # If it's another sort of invalid character, also return False, but print a different message.
            if char == "#":
                pound_count += 1
            else:
                pass

            # If we've got an invalid character that is more than 1 pound or not pound at all, return False. Otherwise
            #     move on.
            if pound_count > 1:
                connection.send_msg(privmsg.chan, "Too many '#'s in channame.")
                return False
            elif pound_count <= 1:
                pass
            else:
                connection.send(privmsg.chan, "Invalid character in channame.")
                return False

    # If we somehow survive all that, return True.
    return True

def valid_pw(connection, privmsg, pw):
    if pw == "":
        return True
    else:
        pass

    for char in pw:
        if char not in alphabet:
            connection.send_msg(privmsg.chan, "Invalid character in given password.")
            return False
        else:
            pass
    return True