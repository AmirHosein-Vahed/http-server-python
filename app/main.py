from HTTP_Server import HTTP_Server
import sys

def main():

    server = HTTP_Server(sys.argv)
    server.start()
    
        

if __name__ == "__main__":
    main()
