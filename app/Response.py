class Response:
    def __init__(self):
        self.headers = ""
        self.status = None
        self.body = ""
        self.static_dir = None

    def set_status(self, status: int):
        self.status = status

    def set_body(self, body: str):
        self.body = body

    def add_header(self, header: dict):
        key = next(iter(header))
        value = header[key]
        self.headers += f"{key}: {value}\r\n"

    def send(self, connection):
        if self.status == None:
            raise Exception("Satus did not set")
        
        elif self.status == 200:
            response = f"HTTP/1.1 200 OK\r\n{self.headers}\r\n{self.body}"

        elif self.status == 201:
            response = f"HTTP/1.1 201 Created\r\n{self.headers}\r\n{self.body}"
        
        elif self.status == 404:
            response = f"HTTP/1.1 404 Not Found\r\n{self.headers}\r\n{self.body}"
            
        self.__send(connection, response)

    def __send(self, connection, response):
        connection.sendall(response.encode())
        connection.close()
            