class Request:
    def __init__(self, connection, address):
        self.connection = connection
        self.address    = address
        self.data       = self.connection.recv(1024).decode().split("\r\n")
        self.method     = self.data[0].split(" ")[0]
        self.URLpath    = self.data[0].split(" ")[1]
        self.http_version = self.data[0].split(" ")[2]
        self.body       = self.data[-1]

    def set_user_agent(self):
        self.user_agent = self.data[2].split(" ")[1]

    def print_data(self):
        print(self.data[-1])
        