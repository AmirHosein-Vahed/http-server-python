import socket
import threading
from typing import Optional, Tuple
from Request import Request
from Response import Response
from Router import router_map

class HTTP_Server:
    """HTTP Server implementation that handles incoming connections and routes requests."""
    
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 4221
    
    def __init__(self, argv: list):
        """
        Initialize the HTTP server.
        
        Args:
            argv: Command line arguments, expecting --directory flag for static files
        """
        self.static_dir: Optional[str] = None
        if len(argv) == 3 and argv[1] == "--directory":
            self.static_dir = argv[2]
        self.server_socket: Optional[socket.socket] = None
            
    def start(self) -> None:
        """Start the HTTP server and begin listening for connections."""
        try:
            self.server_socket = socket.create_server(
                (self.DEFAULT_HOST, self.DEFAULT_PORT),
                reuse_port=True
            )
            print(f"Server listening at {self.DEFAULT_HOST}:{self.DEFAULT_PORT}")
            
            while True:
                self.listen()
                
        except KeyboardInterrupt:
            print("\nShutting down server...")
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()

    def listen(self) -> None:
        """Accept incoming connections and handle them in separate threads."""
        try:
            conn, addr = self.server_socket.accept()
            threading.Thread(
                target=self.handle_request,
                args=(conn, addr),
                daemon=True
            ).start()
        except Exception as e:
            print(f"Error accepting connection: {e}")

    def handle_request(self, connection: socket.socket, address: Tuple[str, int]) -> None:
        """
        Handle an incoming HTTP request.
        
        Args:
            connection: The socket connection
            address: The client address
        """
        try:
            req = Request(connection, address)
            self.route(req)
        except Exception as e:
            print(f"Error handling request from {address}: {e}")
            try:
                resp = Response()
                resp.set_status(500)
                resp.set_body("Internal Server Error")
                resp.send(connection)
            except:
                connection.close()

    def route(self, req: Request) -> None:
        """
        Route the request to the appropriate handler.
        
        Args:
            req: The Request object
        """
        resp = Response()
        resp.static_dir = self.static_dir

        # print("Path ===", self.req.URLpath)

        for method, url, view in router_map:
            if req.method == method:    
                if req.URLpath == url:
                    view(req, resp)
                    break
                elif url.startswith("^") and req.URLpath.startswith(url[1:]):
                    view(req, resp)
                    break

        if resp.status == None:
            resp.set_status(404)

        resp.send(req.connection)
        
