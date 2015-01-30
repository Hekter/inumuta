import sys

class IRCContext:
    def __init__(self, ircsock, comchar, homedir, debugmode, quiet_mode):
        self.ircsock = ircsock
        self.comchar = comchar
        self.homedir = homedir
        self.debugmode = debugmode
        self.quiet_mode = quiet_mode

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

    def names_request(self, chan):
        try:
            self.ircsock.send(str.encode("NAMES " + chan + "\r\n"))
        except OSError:
            print("Unable to send names command request. Program closing.")
            sys.exit()