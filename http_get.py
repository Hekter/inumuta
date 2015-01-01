# I DON'T WANT TO LIVE ANY MORE

import http.server

import http_irc as irc

class myHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        latestMessage = irc.latestMessage.latestMessage
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        self.wfile.write(str.encode(latestMessage))
        return

    def do_POST(self):
        self.send_response(200)
        post_body = self.rfile.read()
        print(str(post_body()))
        return

def get_n_run(server_class=http.server.HTTPServer, handler_class=myHandler,):
    server_address = ('', 54322)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()