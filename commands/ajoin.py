# To muck with databases.
import sqlite3 as lite
# To muck with os.path.join
import os

# For access to valid_chan
import utils

def run(connection, privmsg):
    # Split up the text from privmsg.post_command_text into a list so that it can be addressed one word at a time.
    # However, if there is no chan argument, raise ValueError exception to be handled in privmsg.
    msg = privmsg.post_command_text.split()
    try:
        input_chan = msg[0]
    except IndexError:
        raise ValueError

    if utils.valid_chan(connection, privmsg, input_chan) == True:
        pass
    else:
        return

    # Now to grab the password... potentially. Basically the same shit as with grabbing the chan earlier.
    try:
        pw = msg[1]
    except IndexError:
        pw = ""

    # Prep password for insertion into the SQL database. If it's blank (no password) convert to NULL string for SQL.
    if pw == "":
        pw = "NULL"

    # Parse for invalid chars. If False is returned (invalid)
    else:
        if utils.valid_pw(connection, privmsg, pw) == True:
            pass
        else:
            return

    # With that out of the way, now that we have both chan and the password, let's connect to the database.
    con = lite.connect(os.path.join(connection.homedir, "inumuta.db"))
    with con:
        cur = con.cursor()

        # First we have to check to see whether or not the channel already exists in the database. If it doesn't already
        #     exist in the db (returns None), we can continue on.
        cur.execute("SELECT Name FROM Chans WHERE Name=:ChanName", {"ChanName": input_chan})
        con.commit()

        # Get the contents of the search. Assuming there's not a horrifying error, there should only be
        #     only one entry of a chan.
        row = cur.fetchone()
        if row == None:
            cur.execute("INSERT INTO Chans VALUES(:ChanName,:Password)", {"ChanName": input_chan, "Password": pw})

            # Convert back to non-SQL none-value
            if pw == "NULL":
                pw = ""
            else:
                pass

            # Call joinChan() function to actually send the join command to the channel.
            connection.join_channel(input_chan, pw)

        # If it's already there, send message back to original channel (message loc 2) that is already on ajoin.
        else:
            connection.send_msg(privmsg.chan, "Channel already added to auto-join list.")
            return