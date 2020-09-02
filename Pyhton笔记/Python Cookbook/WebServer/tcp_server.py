from socketserver import BaseRequestHandler, TCPServer

"""
class BaseRequestHandler:

    # Base class for request handler classes.

    # This class is instantiated for each request to be handled.  The
    # constructor sets the instance variables request, client_address
    # and server, and then calls the handle() method.  To implement a
    # specific service, all you need to do is to derive a class which
    # defines a handle() method.

    # The handle() method can find the request as self.request, the
    # client address as self.client_address, and the server (in case it
    # needs access to per-server information) as self.server.  Since a
    # separate instance is created for each request, the handle() method
    # can define other arbitrary instance variables.



    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def setup(self):
        pass

    def handle(self):
        pass

    def finish(self):
        pass
"""

class EchoHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        while True:
            msg = self.request.recv(8192) 
            if not msg: 
                break 
            self.request.send(msg)

if __name__ == '__main__': 
    # __init__(server_address, RequestHandlerClass)
    serv = TCPServer(('', 2333), EchoHandler)   
    serv.serve_forever()