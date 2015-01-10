# A command to highlight the names of everyone in channel and display a message for them to see.

import utils

import debugtools as debug

def run(connection, privmsg):
    connection.send_msg(privmsg.chan, "No.")

def NOPE(connection, privmsg):
    # Empty dictionary for nicks to be added to later.
    nick_dict = {}

    # partialmessage is set to blank for the moment as it's only used lower.
    partialmessage = ""
    # calltext (what we're going to yell at everyone after we ping them) is everything after the @call!
    calltext = privmsg.post_command_text
    debug.echo(connection.debugmode, calltext, "calltext inside run() in call.py")

    # Then we send a NAMES request to the IRC server.
    connection.names_request(privmsg.chan)
    debug.echo(connection.debugmode, privmsg.chan, "privmsg.chan inside run() in call.py")

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
                    # Increment counter by 1.
                    nicklist_count += 1
                elif msg.name == "PRIVMSG":
                    connection.send_msg(privmsg.get_chan(), "I'm busy at the moment with another command! Try again in a jiffy!")
                    break
                elif msg.name == "Code366":
                    for x in list(nick_dict.values()):
                        try:
                            connection.send_msg(privmsg.chan, x)
                        except OSError:
                            raise
                    try:
                        connection.send_msg(privmsg.chan, calltext)
                    except OSError:
                        raise
                    break
                else:
                    pass
            ircmsg = partition[2]
        break

    return