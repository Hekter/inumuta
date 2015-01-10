import debugtools as debug
import random
import time


def run(connection, privmsg):
    instance_random = random.Random()
    values = [1, 5, 10, 20, 25, 45, 50, 75, 100, 150, 200, 250, 300, 350, 400, 450, 500]

    random_number = instance_random.randint(0,99)

    if 0 >= random_number <= 11:
        prize = values[0]
    elif 12 >= random_number <= 21:
        prize = values[1]
    elif 22 >= random_number <= 31:
        prize = values[2]
    elif 32 >= random_number <= 41:
        prize = values[3]
    elif 42 >= random_number <= 51:
        prize = values[4]
    elif 52 >= random_number <= 58:
        prize = values[5]
    elif 59 >= random_number <= 64:
        prize = values[6]
    elif 65 >= random_number <= 69:
        prize = values[7]
    elif 70 >= random_number <= 74:
        prize = values[8]
    elif 75 >= random_number <= 79:
        prize = values[9]
    elif 80 >= random_number <= 83:
        prize = values[10]
    elif 84 >= random_number <= 87:
        prize = values[11]
    elif 88 >= random_number <= 90:
        prize = values[12]
    elif 91 >= random_number <= 93:
        prize = values[13]
    elif 94 >= random_number <= 95:
        prize = values[14]
    elif 96 >= random_number <= 97:
        prize = values[15]
    elif 98 >= random_number <= 99:
        prize = values[16]
    else:
        connection.send_msg(privmsg.chan, "Something broke.")
        debug.echo(connection.debugmode, random_number, "random_number, error (over 99)")
        return

    connection.send_msg(privmsg.chan, "Let's spin the wheel!")
    time.sleep(0.5)
    connection.send_msg(privmsg.chan, "Bishuzzzzzzz")
    time.sleep(0.5)
    connection.send_msg(privmsg.chan, "zzzzz")
    time.sleep(0.75)
    connection.send_msg(privmsg.chan, "tick")
    time.sleep(0.75)
    connection.send_msg(privmsg.chan, "..tick...")
    time.sleep(1)
    connection.send_msg(privmsg.chan, "......tick......")
    time.sleep(1)
    connection.send_msg(privmsg.chan, "Congratulations! The wheel landed on a prize of $" + str(prize) + "!")

    return