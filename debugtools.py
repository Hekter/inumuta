# So that we know the exact microsecond when shit gets whacky.
import datetime
import time

def echo(debugmode, toprint, debugloc):
    if debugmode:
        debugmsg = (str(toprint) + ' Debug Location: ' + debugloc + " " + str(datetime.datetime.utcnow()))
        print(debugmsg)
        time.sleep(0.5)
    else:
        return

def echoToIRC(debugmode, toprint, debugloc, ircsock):
    if debugmode:
        ircsock.send(str.encode(str(toprint) + " Debug Location: " + debugloc + " " + str(datetime.datetime.utcnow())))
    else:
        return

def prompt():
    print('Would you like to invoke DEBUG mode?')
    DEBUGREPLY = str.lower(input())
    if DEBUGREPLY == 'y' or DEBUGREPLY == 'yes':
        print('DEBUG mode activated.')
        return True
    else:
        print('DEBUG activation skipped.')
        return False