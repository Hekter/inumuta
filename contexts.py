import sys

class IRCContext:
    def __init__(self, ircsock, comchar, homedir, debugmode):
        self.ircsock = ircsock
        self.comchar = comchar
        self.homedir = homedir
        self.debugmode = debugmode

    def send_msg(self, chan, msg):
        try:
            self.ircsock.send(str.encode("PRIVMSG " + chan + " :" + msg + "\r\n"))
        except OSError:
            print("Unable to send message to socket. Program closing.")
            sys.exit()

    def join_channel(self, chan, pw):
        try:
            self.ircsock.send(str.encode("JOIN " + chan + " " + pw + "\r\n"))
        except OSError:
            print("Unable to send join message to socket. Program closing.")
            sys.exit()