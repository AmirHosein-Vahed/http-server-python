import socket
from Request import Request
from Response import Response
import threading

class HTTP_Server:
    def __init__(self):
        pass

    def start(self):
        server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
        self.server_socket = server_socket
        print("Server listening at 127.0.0.1:4221")

    def listen(self):

        conn, addr = self.server_socket.accept()
        threading.Thread(target=self.handle_request, args=(conn, addr,)).start()
        # self.req = Request(conn, addr)
        # self.route()

    def handle_request(self, connection, address):
        self.req = Request(connection, address)
        self.route()

    def route(self):
        self.resp = Response()

        if self.req.URLpath == "/":
            self.resp.set_status(200)

        elif self.req.URLpath == "/index.html":
            self.resp.set_status(200)
        
        elif self.req.URLpath == "/user-agent":
            self.resp.set_status(200)
            # self.req.print_data()
            self.req.set_user_agent()
            self.resp.add_header({"Content-Type": "text/plain"})
            self.resp.add_header({"Content-Length": len(self.req.user_agent)})
            self.resp.set_body(self.req.user_agent)
        
        elif self.req.URLpath.startswith("/echo/"):
            arg = self.req.URLpath.split("/")[2]
            self.resp.set_status(200)
            self.resp.add_header({"Content-Type": "text/plain"})
            self.resp.add_header({"Content-Length": len(arg)})
            self.resp.set_body(arg)
        
        else:
            self.resp.set_status(404)

        self.resp.send(self.req.connection)

