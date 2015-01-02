import formats

alphabet = "abcdefghijklmnopqrstuvwxyz"

def getMsgClass(msg):
    """START THE IF TREE"""

    # Now we start a big ole if tree to find out if the message is a type we care about / can handle.
    # If so, we instantiate its class which contains how to do what it needs.
    if msg[1] == 'PRIVMSG':
        msgtype = formats.Privmsg(msg)
        return msgtype
    elif msg[0] == 'PING':
        msgtype = formats.Ping(msg)
        return msgtype
    elif msg[1] == '353':
        msgtype = formats.code353(msg)
        return msgtype
    elif msg[1] == '366':
        msgtype = formats.code366(msg)
        return msgtype
    else:
        return None

    # Now we make sure there aren't any invalid characters in our chan var :3
    # We set pound_count to 0 to ... count the # of #s :P We already established above we have at least 1, now to check
    #     and make sure there isn't any more than that.
def valid_chan(connection, privmsg, input_chan):
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
                connection.send(privmsg.chan, "Too many #s in channame.")
                return False
            elif pound_count <= 1:
                pass
            else:
                connection.send(privmsg.chan, "Invalid character in channame.")
                return False

    # If we somehow survive all that, return True.
    return True