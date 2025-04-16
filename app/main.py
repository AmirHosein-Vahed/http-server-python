import socket  # noqa: F401


def path_matched(path: str) -> bool:
    if path in ["/", "/index.html"]:
        return True
    else:
        return False


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server listening at 127.0.0.1:4221")

    while True:
        conn, addr = server_socket.accept() # wait for client connection

        data = conn.recv(1024).decode()
        URLpath = data.split("\r\n")[0].split(" ")[1]

        response = b"HTTP/1.1 200 OK\r\n\r\n"
        if not path_matched(URLpath):
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"

        conn.sendall(response)
        conn.close()
            
    


if __name__ == "__main__":
    main()
