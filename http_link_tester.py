# BECAUSE I DON'T KNOW HOW TO LUA
# AT ALL

import urllib.request
import urllib.parse

data = urllib.parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
data = data.encode('utf-8')
request = urllib.request.Request("http://localhost:54321")
# adding charset parameter to the Content-Type header.
request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
f = urllib.request.urlopen(request, data)
print(f.read().decode('utf-8'))
