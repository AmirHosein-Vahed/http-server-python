from HTTP_Server import HTTP_Server


def handle_thread():
    pass

def main():

    server = HTTP_Server()
    server.start()

    while True:
        server.listen()
        

if __name__ == "__main__":
    main()
