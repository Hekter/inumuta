import world

def run(connection, privmsg):
    connection.valid_commands = world.loadCommands(connection.commandpath)
    return