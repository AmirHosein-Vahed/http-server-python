import socket
from typing import List, Optional

class Request:
    """HTTP Request handler class that parses incoming HTTP requests."""
    
    def __init__(self, connection: socket.socket, address: tuple):
        """
        Initialize a new Request object.
        
        Args:
            connection: The socket connection object
            address: The client address tuple
        """
        self.connection = connection
        self.address = address
        self.data: List[str] = self.connection.recv(1024).decode().split("\r\n")
        
        # Parse the request line
        request_line = self.data[0].split(" ")
        self.method: str = request_line[0]
        self.URLpath: str = request_line[1]
        self.http_version: str = request_line[2]
        
        self.body: str = self.data[-1]
        self.user_agent: Optional[str] = None

    def set_user_agent(self) -> None:
        """Extract and set the User-Agent header from the request."""
        for header in self.data[1:]:
            if header.lower().startswith("user-agent:"):
                self.user_agent = header.split(" ", 1)[1]
                break

    def get_header(self, header_name: str) -> Optional[str]:
        """
        Get a specific header value from the request.
        
        Args:
            header_name: The name of the header to retrieve
            
        Returns:
            The header value if found, None otherwise
        """
        header_name = header_name.lower()
        for header in self.data[1:]:
            if header.lower().startswith(f"{header_name}:"):
                return header.split(" ", 1)[1]
        return None

    def print_data(self):
        print(self.data[-1])
        