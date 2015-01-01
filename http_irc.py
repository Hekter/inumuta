import socket
import sys
import time

from threading import Lock
from threading import Thread

lock = Lock()
threads = []

BOTNICK = "ComputerCraft"

class LatestMessage:
    def __init__(self):
        self.latestMessage = ''

latestMessage = LatestMessage()

def irc_receiver(ircsock):
    while True:
        ircmsg = bytes.decode(ircsock.recv(2046)).strip('\r\n')
        print(ircmsg)

        # Split the received message into a list.
        ircmsg = ircmsg.split()
        print(str(ircmsg))

        # Part of IRC authentication and connection-monitoring, PINGs must be responded to with PONGs
        if ircmsg[0] == "PING":
            ircsock.send(str.encode("PONG " + ircmsg[1] + "\r\n"))
            print("PONG " + ircmsg[1])
        else:
            try:
                if ircmsg[1] == "PRIVMSG":
                    lock.acquire()
                    latestMessage.latestMessage = " ".join(ircmsg[3:])[1:]
                    lock.release()
                    print(str(latestMessage.latestMessage))
                else:
                    pass
            except IndexError:
                sys.exit()

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    ircsock.connect(("198.100.123.140", 6667))
except Exception as error:
    print("Unable to connect to server.")
    print(str(error))
    sys.exit()

t = Thread(target=irc_receiver, args=(ircsock,))
threads.append(t)
t.start()

# IRC protocol dicatates we have to identify ourselves with username nonsense.
# We sleep for two seconds to let the IRC server catch up to us, otherwise we move too fast and stuff gets lost.
ircsock.send(str.encode("USER " + str(socket.gethostname()) + " 0 * :" + BOTNICK + "Bot\r\n"))
time.sleep(2)

# Next IRC protocol says we need to establish a nickname.
ircsock.send(str.encode("NICK " + BOTNICK + "\r\n"))
time.sleep(2)