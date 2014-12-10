# So that we know the exact microsecond when shit gets whacky.
import datetime as time

def echo(debugmode, toprint, debugloc):
    if debugmode == True:
        print((str(toprint) + ' Debug Location: ' + debugloc), end=' ')
        print(time.datetime.utcnow())
    else:
        return

def echoToIRC(debugmode, toprint, debugloc, ircsock):
    if debugmode == True:
        ircsock.send(str.encode(str(toprint) + " Debug Location: " + debugloc + " " + str(time.datetime.utcnow())))
    else:
        return

def prompt():
    print('Would you like to invoke DEBUG mode?')
    DEBUGREPLY = str.lower(input())  # Fuck your upper case in its beady little eyes.
    if DEBUGREPLY == 'y' or DEBUGREPLY == 'yes':
        print('DEBUG mode activated.')
        return True
    else:
        print('DEBUG activation skipped.')
        return False