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