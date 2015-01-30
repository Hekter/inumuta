# A command to highlight everyone in the channel and display an input message for them to see.

import utils

import debugtools as debug


class Call:
    # Container class for retaining values needed for calling everything evar!

    def __init__(self, calltext):

        # Store the input calltext.
        self.calltext = calltext

        # Establish which "classes" of messages we want to act on.
        self.activate_on = ["Code366", "Code353", "PRIVMSG"]

        # Empty dictionary to store nicks into.
        self.nick_dict = {}

    def run(self, connection, received_message):
        print("FIRE, FIRE IN THE COURTHOUSE!")


def run(connection, privmsg):

    # Instantiate the Call class and feed it the post_command_text
    call = Call(privmsg.post_command_text)

    # Now we add add the Call class to the connection.processQ list.
    connection.processQ.append(call)