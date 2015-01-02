import debugtools
import world

class Privmsg:
    def __init__(self, ircmsg):
        self.name = 'PRIVMSG'
        self.fullmsg = ircmsg
        self.isCommand = True
    def do(self, connection):

        # Reassign msg to just "#chan" and ":text" and "here for the message" strings
        self.msg = self.fullmsg[2].split(sep=None, maxsplit=2)
        debugtools.echo(connection.debugmode, self.msg, "self.msg after the reassign split shenanigans.")

        # Set chan variable to msg[0] which contains where the message came from.
        self.chan = self.msg[0]
        debugtools.echo(connection.debugmode, self.chan, "self.chan")

        # See if the commandchar string is located inside self.msg[1]
        debugtools.echo(connection.debugmode, self.msg[1], "self.msg[1] before if checking for commandchar string.")
        if connection.comchar in self.msg[1]:

            # Set the command variable to the rest of the characters in the [1] slot in msg besides the first two.
            # This cuts off the :@ and leaves us with a regular string. Also lowers the case it.
            command = self.msg[1][2:].lower()
            debugtools.echo(connection.debugmode, command, "command inside the if.")

            # Check and see if the valid command is in valid_commands
            if command in connection.valid_commands:

                # If command listed in valid_commands, dynamically import the .py file with the same name as runcommand
                runcommand = __import__(command)

                try:
                    runcommand.run(connection, self)
                except ValueError:
                    connection.send_msg(self.chan,"Too few arguments. Unable to execute " + command + " command.")

            # Now check for special, built-in commands.
            elif command == "reload":
                connection.valid_commands = world.loadCommands(connection.commandpath)
            elif command == "debug-on":
                connection.debugmode = True
            elif command == "debug-off":
                connection.debugmode = False
            else:
                connection.send_msg(self.chan, "Invalid command!")
        else:
            pass


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