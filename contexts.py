class IRCContext:
    def __init__(self, sockconn, homedir):
        self.sockconn = sockconn
        self.homedir = homedir
        self.connected_chans = []

    def getType(self, msg):
        msgType = msg[1]


    # def argGrabber(self, msg, argNum):
    #     argResults = []
    #     for x in range(1, argNum + 1):
    #         try:
    #             argResults.append(msg[3 + x])
    #         except IndexError:
    #             argResults.append(None)
    #     return argResults