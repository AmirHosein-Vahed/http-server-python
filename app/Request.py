class Request:
    def __init__(self, connection, address):
        self.connection = connection
        self.address    = address
        self.data       = self.connection.recv(1024).decode().split("\r\n")
        self.URLpath    = self.data[0].split(" ")[1]
        self.user_agent = self.data[2].split(" ")[1]
        
    def print_data(self):
        print("data: ", self.data)