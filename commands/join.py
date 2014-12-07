import world
import sqlite3 as lite
import os

# passGrab grabs the password if it exists after a "@join #channame" command
# If there is no password, return string "NULL"
def passGrab(chan, msg):
    print("msg VAR IS " + str(msg))
    print("chan VAR IS " + str(chan))
    chanloc = msg.find(chan)
    print("chanlock VAR IS " + str(chanloc))
    pw = msg[(chanloc + len(chan)):]
    print("pw VARIABLE IS " + str(pw))
    if pw == '':
        return "NULL"
    else:
        for x in pw:
            if x not in world.validchars:

                # Return with an invalid char in the return statement so that InvalidChar can be used as a pw
                #     for whatever the fuck reason.
                return "!InvalidChar"
            else:
                return pw

# # ircJoin actually sends the IRC command to join a room
# def ircJoin(ircsock, chan):
#     try:
#         ircsock.send(str.encode("JOIN " + chan))
#     except OSError:
#         return "broked"

# Default run() command. This command tells the bot to join a channel
def run(ircsock, msg):

    # Use the world.changrab() method to get the channel name. See world for documentation on how this works.
    # We only pass everything past ":@join" because otherwise we pick up the chan name of the channel we're already in
    chan = world.changrab(msg[msg.find(":@join"):])
    print(str(chan))

    # Check to see if changrab returned None (no channel found)
    if chan == None:
        return None
    else:
        pass

    # Use the local method passGrab() to get the password if there is any! If not, pass NULL
    # Also prints invalidchar message if relevant.
    pw = passGrab(chan, msg)
    if pw == "!InvalidChar":
        world.sendmsg(ircsock, chan, "Invalid character in password argument.")
        return None
    # elif pw == '':
    #     pw = "NULL"
    else:
        pass

    # Go up a directory to connect to inumuta.db which is located inside /trunk
    os.chdir(os.pardir)

    # Connect to inumuta.db
    con = lite.connect("inumuta.db")
    with con:
        cur = con.cursor()

        # Here we are checking to see if the channel already exists in the database. It attempts to select the name
        #     of the channel from the existing entries. If it doesn't exist (returns None), we continue with adding.
        cur.execute("SELECT Name FROM Chans WHERE Name=:ChanName", {"ChanName": chan})
        con.commit()

        row = cur.fetchone()
        if row == None:
            cur.execute("INSERT INTO Chans VALUES(:ChanName,:Password)", {"ChanName": chan, "Password": pw})

            # Call ircJoin to actually send message to join channel to the irc chan.
            world.joinchan(ircsock, chan, pw)
        else:
            world.sendmsg(ircsock, chan, "Channel already added to join list!")
    return