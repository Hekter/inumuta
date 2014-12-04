# Import sqlite3 for... database mucking!
import sqlite3 as lite

# Standard function call. Creates inumuta.db if it doesn't exist (which is a prerequisite for this getting called)
#     and creates the relevant tables therein.
def run():
    con = lite.connect('inumuta.db')
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE Chans(Name TEXT, Password TEXT)")
        cur.execute("CREATE TABLE AuthorizedUsers(Name TEXT)")
        cur.execute("CREATE TABLE Orders(PrioNumber INT, PrioTitle TEXT, PrioLink TEXT, AdditionalText TEXT)")