# A command to highlight everyone in the channel and display an input message for them to see.

import utils

import debugtools as debug


class Call:
    # Container class for retaining values needed for calling everything evar!

    def __init__(self, calltext, chan):

        # Store the input calltex and incoming chan that we want to hook into.
        self.calltext = calltext
        self.chan = chan

        # Establish which "classes" of messages we want to act on.
        self.activate_on = ["Code366", "Code353"]

        # Empty dictionary to store nicks based on in which "batch" they are received.
        self.nick_dict = {}

        # Start the count for creating the dictionary keys at 1
        self.nicklist_count = 1

        # Are we finished? Nevar!
        self.finished = False

    def run(self, connection, received_message):

        # Check to see if the received message packet has the chan that we are looking for!
        if received_message.get_chan() != self.chan:
            return
        else:
            pass

        if received_message.name == "Code353":
            self.code353(connection, received_message)
        elif received_message.name == "Code366":
            self.code366(connection)
        else:
            print("Unable to execute command. Horrible errors are afoot.")

    def code353(self, connection, received_message):
        nicks = received_message.get_nicks()
        debug.echo(connection.debugmode, nicks, "nicks inside elif code353")
        self.nick_dict[self.nicklist_count] = nicks
        debug.echo(connection.debugmode, self.nick_dict, "nick_dict")
        # Increment counter by 1.
        self.nicklist_count += 1

    def code366(self, connection):
        debug.echo(connection.debugmode, list(self.nick_dict.values()), "list(nick_dict.values())")
        for x in list(self.nick_dict.values()):
            try:
                connection.send_msg(self.chan, x)
            except OSError:
                raise
        try:
            connection.send_msg(self.chan, self.calltext)
        except OSError:
            raise

        self.finished = True




def run(connection, privmsg):

    # Instantiate the Call class and feed it the post_command_text
    call = Call(privmsg.post_command_text, privmsg.chan)

    # Now we add add the Call class to the connection.processQ list.
    connection.processQ.append(call)

    # Send the actual NAMES request to the IRC server.
    connection.names_request(privmsg.chan)

    return