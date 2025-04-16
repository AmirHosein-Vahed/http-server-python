class Request:
    def __init__(self, connection, address):
        self.connection = connection
        self.address    = address
        self.data       = self.connection.recv(1024).decode().split("\r\n")
        self.URLpath    = self.data[0].split(" ")[1]