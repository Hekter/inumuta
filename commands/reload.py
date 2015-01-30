import msg_receive

def run(connection, privmsg):
    connection.valid_commands = msg_receive.loadCommands(connection.commandpath)
    return