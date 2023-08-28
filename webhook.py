#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
import logging
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

grey = "\x1b[38;20m"
yellow = "\x1b[33;20m"
green = "\x1b[32;20m"
red = "\x1b[31;20m"
bold_red = "\x1b[31;1m"
reset = "\x1b[0m"

consoleHandler = logging.StreamHandler()
formatter = logging.Formatter(f"""%(asctime)s - %(levelname)s - %(name)s
--------------------------------------- request ---------------------------------------
{green}%(method)s %(path)s{reset}
%(headers)s
{yellow}%(data)s{reset}
-----------------------------------
"""
                              )
consoleHandler.setFormatter(formatter)
consoleHandler.setLevel(logging.INFO)

logger = logging.getLogger('http-request')
logger.setLevel(logging.INFO)
logger.addHandler(consoleHandler)

class S(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        json_obj = json.loads(post_data.decode('utf-8'))
        json_data = json.dumps(json_obj, indent=2)
        logger.info(msg="Request content", extra={
            'method': "POST",
            'path': str(self.path),
            'headers': str(self.headers),
            'data': json_data
        })
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

    def log_message(self, format, *args):
        pass


def run(server_class=HTTPServer, handler_class=S, port=9052):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

run()

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()