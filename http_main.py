# This is insanity and I have no idea why am do.
# YOLOSWAG

import socket
import sys
import threading
import time

import http_get as get

threads = []

def receiver(connect):
    httpmsg = bytes.decode(connect.recv(2048))

    print(httpmsg + "httpmessage before split")

    httpmsg = httpmsg.split('\r\n')

    print(str(httpmsg) + " httpmsg")

    if ":key:" in httpmsg[0]:
        print(str(httpmsg) + " YOU DA REAL MVP")
        connect.send(str.encode("POST / HTTP/1.1 / 200"))
        return
    else:
        try:
            if ":key:" in httpmsg[8]:
                print(str(httpmsg) + " YOU DA REAL MVP")
                connect.send(str.encode("POST / HTTP/1.1 / 200"))
                return
            elif ":key:" in httpmsg[9]:
                print(str(httpmsg) + " YOU DA REAL MVP")
                connect.send(str.encode("POST / HTTP/1.1 / 200"))
                return
            else:
                pass
        except IndexError:
            pass

    return

httpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    httpsock.bind(('', 54321))
except Exception as error:
    print("Unable to create server.")
    print(str(error))
    sys.exit()

t = threading.Thread(target=get.get_n_run())
threads.append(t)
t.start()

httpsock.listen(10)

while True:
    time.sleep(0)
    connection, addr = httpsock.accept()
    print("Client connected from " + str(addr[0]) + ":" + str(addr[1]) + ".")
    t = threading.Thread(target=receiver, args=(connection,))
    threads.append(t)
    t.start()