import world
import sqlite3 as lite
import os
import sendmsg

# passGrab grabs the password if it exists after a "@join #channame" command
def passGrab(chan, msg):
    chanloc = msg.find(chan)


# Default run() command. This command tells the bot to join a channel
def run(ircsock, msg):

    # Use the world.changrab() method to get the channel name. See world for documentation on how this works.
    chan = world.changrab(msg)

    # Check to see if changrab returned None (no channel found)
    if chan == None:
        return None
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
            cur.execute("INSERT INTO Chans VALUES(?,?)")
        else:
            print(row[0])