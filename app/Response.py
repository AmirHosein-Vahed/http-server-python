from typing import Dict, Optional
from http import HTTPStatus

class Response:
    """HTTP Response handler class that builds and sends HTTP responses."""
    
    def __init__(self):
        """Initialize a new Response object with empty headers and body."""
        self.headers: str = ""
        self.status: Optional[int] = None
        self.body: str = ""
        self.static_dir: Optional[str] = None

    def set_status(self, status: int) -> None:
        """
        Set the HTTP status code for the response.
        
        Args:
            status: The HTTP status code (e.g., 200, 404)
        """
        if status not in [s.value for s in HTTPStatus]:
            raise ValueError(f"Invalid HTTP status code: {status}")
        self.status = status

    def set_body(self, body: str) -> None:
        """
        Set the response body.
        
        Args:
            body: The content to be sent in the response body
        """
        self.body = body

    def add_header(self, header: Dict[str, str]) -> None:
        """
        Add a header to the response.
        
        Args:
            header: A dictionary containing a single header key-value pair
        """
        if len(header) != 1:
            raise ValueError("Header dictionary must contain exactly one key-value pair")
        
        key = next(iter(header))
        value = header[key]
        self.headers += f"{key}: {value}\r\n"

    def send(self, connection) -> None:
        """
        Send the complete HTTP response through the connection.
        
        Args:
            connection: The socket connection to send the response through
            
        Raises:
            Exception: If status code is not set
        """
        if self.status is None:
            raise Exception("Status code must be set before sending response")
        
        status_line = f"HTTP/1.1 {self.status} {HTTPStatus(self.status).name}\r\n"
        response = f"{status_line}{self.headers}\r\n{self.body}"
        
        self.__send(connection, response)

    def __send(self, connection, response: str) -> None:
        """
        Internal method to send the response and close the connection.
        
        Args:
            connection: The socket connection
            response: The complete HTTP response string
        """
        connection.sendall(response.encode())
        connection.close()
            