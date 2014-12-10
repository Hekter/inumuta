def run(ircsock, msg, homedir):
    chan = msg[2]
    ircsock.send(str.encode("PRIVMSG " + chan + " :Hello! I WILL DESTROY YOU.\r\n"))
    return None