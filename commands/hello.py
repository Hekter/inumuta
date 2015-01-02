def run(connection, privmsg):
    connection.send_msg(privmsg.chan, "Hello! I WILL DESTROY YOU.")
    return None