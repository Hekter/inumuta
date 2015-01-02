def run(connection):
    connection.ircsock.send(str.encode("PRIVMSG " + connection.chan + " :Hello! I WILL DESTROY YOU.\r\n"))
    return None