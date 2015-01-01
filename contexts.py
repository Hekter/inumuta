class IRCContext:
    def __init__(self, ircsock, comchar, homedir):
        self.ircsock = ircsock
        self.comchar = comchar
        self.homedir = homedir