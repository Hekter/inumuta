class Privmsg:
    def __init__(self, msg):
        self.name = 'PRIVMSG'
        self.msg = msg
        self.isCommand = False


class Ping:
    def __init__(self, msg):
        self.name = 'PING'
        self.msg = msg
        self.isCommand = True
    def do(self, connection):
        connection.ircsock.send(str.encode("PONG " + self.msg[1] + "\r\n"))


# class Join:
#     def __init__(self, msg):
#         pass
#
#
# class Part:
#     def __init__(self, msg):
#         pass


class code353:
    def __init__(self, msg):
        self.name = 'Code353'


class code366:
    def __init__(self, msg):
        self.name = 'Code366'