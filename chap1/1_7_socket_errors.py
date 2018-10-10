import sys
import socket
import argparse

def main():
    # setup argument parsing
    parser =  argparse.ArgumentParser(description='Socket Error Exs')
    parser.add_argument('--host', action='store', dest='host', required=False)
    parser.add_argument('--port', action='store', dest='port', type=int, required=False)
    parser.add_argument('--file', action='store', dest='file', required=False)
    given_args = parser.parse_args()
    host = given_args.host
    port = given_args.port
    filename = given_args.file

    # First try_except block -- create socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.gaierror as e:
        print('Address-related error connection to server: ', f'{e}')
        sys.exit(1)
    except socket.error as e:
        print("Connection error: ", f'{e}')
        sys.exit(1)

    # Third try_except block -- sending data
    try:
        message = "GET %s HTTP/1.0\r\n\r\n" % filename
        print(message)
        s.sendall(message.encode())
    except socket.error as e:
        print("Error sending data : ", f'{e}')
        sys.exit(1)

    while 1:
        # Fourth try_except block -- waiting to receive data from remote host
        try:
            buf = s.recv(2048)
        except socket.error as e:
            print("Error receiving data: ", f'{e}')
            sys.exit(1)
        if not len(buf):
            break 
        # write the received data
        sys.stdout.write(buf)

if __name__ == '__main__':
    main()

