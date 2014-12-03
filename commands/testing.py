import world

def run(ircsock, msg):
    chan = world.changrab(msg)
    ircsock.send(str.encode("PRIVMSG " + chan + " :This is a test!\r\n"))
    return None