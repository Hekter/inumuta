# WOO

def run(connection, privmsg):
    on_or_off = privmsg.post_command_text.strip()

    if on_or_off == "on":
        connection.debugmode = True
    elif on_or_off == "off":
        connection.debugmode = False
    else:
        connection.send_msg(privmsg.chan, "Invalid argument. Only 'on' or 'off' are accepted.")

    return