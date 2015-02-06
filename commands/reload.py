import utils

def run(connection, privmsg):
    connection.valid_commands = utils.loadCommands(connection.commandpath)
    return