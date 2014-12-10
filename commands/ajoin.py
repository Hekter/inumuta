# To muck with databases.
import sqlite3 as lite
# To muck with os.path.join
import os

# For access to argGrabber
import world

def run(ircsock, msg, homedir):
    # Parse the chan by using the argGrabber (since the channel is technically an argument)
    # Position here in the message list is 4 since it comes after the command (position 3)
    # However if it returns nothing (failure condition in this case), return with invalidArg
    chan = world.argGrabber(msg, 4)
    if chan == '':
        return "invalidArg"
    else:
        pass

    # Now we make sure there aren't any invalid characters in our chan var :3
    for char in chan:
        if char in world.VALIDCHARS:
            pass
        else:
            return "invalidArg"

    # Now to grab the password! It'll be in position 5 if there is one.
    pw = world.argGrabber(msg, 5)

    # Prep password for insertion into the SQL database. If it's blank (no password) convert to NULL string for SQL.
    if pw == '':
        pw = "NULL"

    # Parse for invalid chars.
    else:
        for char in pw:
            if char in world.VALIDCHARS:
                pass
            else:
                return "invalidArg"

    # With that out of the way, now that we have both chan and the password, let's connect to the database.
    con = lite.connect(os.path.join(homedir, "inumuta.db"))
    with con:
        cur = con.cursor()

        # First we have to check to see whether or not the channel already exists in the database. If it doesn't already
        #     exist in the db (returns None), we can continue on.
        cur.execute("SELECT Name FROM Chans WHERE Name=:ChanName", {"ChanName": chan})
        con.commit()

        # Get the contents of the search. Assuming there's not a horrifying error, there should only be
        #     only one entry of a chan.
        row = cur.fetchone()
        if row == None:
            cur.execute("INSERT INTO Chans VALUES(:ChanName,:Password)", {"ChanName": chan, "Password": pw})

            # Convert back to non-SQL none-value
            if pw == "NULL":
                pw = ""
            else:
                pass

            # Call joinChan() function to actually send the join command to the channel.
            world.joinChan(ircsock, chan, pw)

        # If it's already there, send message back to original channel (message loc 2) that is already on ajoin.
        else:
            world.sendmsg(ircsock, world.argGrabber(msg, 2), "Channel already added to auto-join list.")