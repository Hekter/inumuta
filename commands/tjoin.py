import world

def run(ircsock, msg, homedir):
    chan = world.argGrabber(msg, 4)
    if chan == '':
        return "invalidArg"
    else:
        pass

    # Now we make sure there aren't any invalid characters in our chan var :3
    for char in chan:
        if char in world.VALIDCHARS:
            pass
        else:
            return "invalidArg"

    # Now to grab the password! It'll be in position 5 if there is one.
    pw = world.argGrabber(msg, 5)

    # Prep password for insertion into the SQL database. If it's blank (no password) convert to NULL string for SQL.
    if pw == '':
        pass

    # Parse for invalid chars.
    else:
        for char in pw:
            if char in world.VALIDCHARS:
                pass
            else:
                return "invalidArg"

    # Call joinChan() function to actually send the join command to the channel.
    world.joinChan(ircsock, chan, pw)