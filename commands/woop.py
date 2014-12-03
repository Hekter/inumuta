import world

print("WOOP WOOP WOOP")

def run(ircsock, msg):
    chan = world.changrab(msg)
    ircsock.send(str.encode("PRIVMSG " + chan + " :WOOP WOOP WOOP WOOP.\r\n"))
    return None