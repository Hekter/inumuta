inumuta
=======

IRC Bot nonsense

Eventually maybe a swap-in replacement for https://github.com/MikeOntry/Sovereign2

How To Use
===

Requires Python 3. Would recommend 3.3 and upwards since that's what I used, but probably works with regular ole 3.

Download and modify settings.ini to fit your server, nick, et-cetera. Make sure to feed it a default room to join or
else you'll have trouble issuing commands! By default the commandchar is "@" but it can be changed to any character,
though I recommend a special character other than a colon. Inumuta will only check the beginning of a PRIVMSG for a
commandchar.

If you want to add additional functionality, continue forth onto a dark and scary path.

Adding Functionality
===

Command scripts can be dropped into the /commands folder even while the bot is running--issue the special command
"@reload" (or whatever your commandchar is instead of @) to refresh the list of valid commands.

Commands are loaded from the /commands folder and dynamically imported when they are 'called'. "@tjoin" invoked at the 
beginning of an IRC PRIVMSG will first check to make sure it [tjoin] is a valid command, then if it is, it will import 
the commands/tjoin.py file and run its run() function, passing in the contexts.IRCContext class instantiation. Therein
you will find all sorts of variables and methods that can be utilized to different ends. See contexts.py for more
documentation in this regard.