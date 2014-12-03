import world

print("JAJAJKLJARKE")

def run(ircsock, msg):
    chan = world.changrab(msg)
    ircsock.send(str.encode("PRIVMSG " + chan + " :Hello! I WILL DESTROY YOU.\r\n"))
    return None