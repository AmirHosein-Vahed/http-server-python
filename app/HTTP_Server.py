import socket
from Request import Request
from Response import Response
from Router import router_map
import threading

class HTTP_Server:
    def __init__(self, argv: list):
        self.static_dir = None
        if len(argv) == 3 and argv[1] == "--directory":
            self.static_dir = argv[2]
            
    def start(self):
        server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
        self.server_socket = server_socket
        print("Server listening at 127.0.0.1:4221")
        
        while True:
            self.listen()

    def listen(self):
        conn, addr = self.server_socket.accept()
        threading.Thread(target=self.handle_request, args=(conn, addr,)).start()

    def handle_request(self, connection, address):
        self.req = Request(connection, address)
        self.route()

    def route(self):
        self.resp = Response()
        self.resp.static_dir = self.static_dir

        # print("Path ===", self.req.URLpath)

        for method, url, view in router_map:
            if self.req.method == method:    
                if self.req.URLpath == url:
                    view(self.req, self.resp)
                    break
                elif url.startswith("^") and self.req.URLpath.startswith(url[1:]):
                    view(self.req, self.resp)
                    break

        if self.resp.status == None:
            self.resp.set_status(404)

        self.resp.send(self.req.connection)
        
