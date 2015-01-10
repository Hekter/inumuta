import debugtools as debug
import utils
import random

# Woooo! Gaming functionality.

def run(connection, privmsg):

    instance_random = random.Random()

    nick_dict = {}

    partialmessage = ""

    # Send the names request!
    connection.names_request(privmsg.chan)

    # BJLEGH
    while True:
        # Need a counter to assign keys to the dictionary! Starting at 1 because why not.
        nicklist_count = 1
        # Wait for a response...
        try:
            ircmsg = bytes.decode(connection.ircsock.recv(1024))
        except OSError:
            print("Unable to receive message on socket. Exiting.")
            raise

        # # No matter what, print what we received!
        # print(ircmsg)
        debug.echo(connection.debugmode, ircmsg, "ircmsg")

        while True:
            ircmsg = partialmessage + ircmsg
            partition = ircmsg.partition("\r\n")
            debug.echo(connection.debugmode, str(partition), "partition")
            if partition[1] == "":
                partialmessage = partition[0]
                break
            else:
                # Then we get and assign a message class to the message! Wee.
                msg = utils.getMsgClass(partition[0])
                debug.echo(connection.debugmode, msg, "msg object after coming back from utils.getMsgClass")

                # If utils.getMsgClass() returns None, it means it's an unsupported/unparsed message type, so we
                #     should loop back to the start.
                if msg is None:
                    pass
                elif msg.name == "Code353":
                    nicks = msg.get_nicks()
                    debug.echo(connection.debugmode, nicks, "nicks inside elif code353")
                    nick_dict[nicklist_count] = nicks
                    debug.echo(connection.debugmode, nick_dict, "nick_dict")
                    # Increment counter by 1.
                    nicklist_count += 1
                elif msg.name == "PRIVMSG":
                    connection.send_msg(privmsg.get_chan(), "I'm busy at the moment with another command! Try again in a jiffy!")
                    break
                elif msg.name == "Code366":
                    for x in list(nick_dict.values()):
                        nicks = []
                        nicksplit = x.split()
                        for y in nicksplit:
                            nicks.append(y)

                    nick_id = instance_random.randint(0, (len(nicks) - 1))
                    selected_nick = nicks[nick_id]

                    try:
                        connection.send_msg(privmsg.chan, selected_nick + ", you're our lucky contestant today!")
                    except OSError:
                        raise
                    break
                else:
                    pass
            ircmsg = partition[2]
        break