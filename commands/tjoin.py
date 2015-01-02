import utils

def run(connection, privmsg):
    # Set the channame to the first word after the command string.
    msg = privmsg.post_command_text.split()

    try:
        input_chan = msg[0]
    except IndexError:
        raise ValueError

    # Now we make sure there aren't any invalid characters in our chan var :3
    if utils.valid_chan(connection, privmsg, input_chan) == True:
        pass
    else:
        return

    # Now to grab the password! It'll be in position 1 if there is one.
    try:
        pw = msg[1]
    except IndexError:
        pw = ""

    if utils.valid_pw(connection, privmsg, pw) == True:
        pass
    else:
        return

    # Call joinChan() function to actually send the join command to the channel.
    connection.join_channel(input_chan, pw)