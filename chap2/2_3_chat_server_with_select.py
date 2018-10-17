import select
import socket
import sys
import signal
import pickle
import struct
import argparse

SERVER_HOST = 'localhost'
CHAT_SERVER_NAME = 'server'

# Some utilities
def send(channel, *args):
    buffer = pickle.dumps(args) # serializer
    value = socket.htonl(len(buffer))
    size = struct.pack("L", value) # data 크기 결정
    channel.send(size)
    channel.send(buffer)

def receive(channel):
    size = struct.calcsize("L")
    size = channel.recv(size)
    try:
        size = socket.ntohl(struct.unpack("L", size)[0])
    except struct.error as e:
        return ''
    buf = ''
    while len(buf) < size:
        buf = channel.recv(size - len(buf))
    return pickle.loads(buf)[0]

'''
데이터 속성 초기화
일반적인 소켓 생성시 같은 포트 재사용 옵션 설정
백로그 인자를 생성자에게 설정해 서버가 응답 대기할 수 있는 연결의 최댓값을 설정
signal 모듈을 사용해 인터럽트를 처리
'''

class ChatServer(object):

    ''' An example chat server using select '''
    def __init__(self, port, backlog=5):
        self.clients = 0
        self.clientmap = {}
        self.outputs = [] # list output sockets
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        print("Server listening to port: %s .." % port)
        self.server.listen(backlog)
        # Catch keyboard interrupts
        signal.signal(signal.SIGINT, self.sighandler)

    def sighandler(self, signum, frame):
	    ''' Clean up client outputs '''
	    # close the server
	    print('Shutting down server...')
	    # close existing client sockets
	    for output in self.outputs:
		    output.close()
	    self.server.close()

    def get_client_name(self, client):
	    ''' return the name of the client '''
	    info = self.clientmap[client]
	    host, name = info[0][0], info[1]
	    return '@'.join((name, host))

	    '''
	    select의 입력 매개변수로 사용할 리스트에 채팅 서버의 소켓과 stdin을 등록한다.
	    select는 반환시 readable, writeable, except 등 총 3개의 소켓 리스트를 제공한다.
	    서버는 클라이언트의 이름을 얻어 다른 모든 클라이언트에게 전송한 후, 이 클라이언트의 소켓을 select 호출에서 사용할 입력 매개변수 리스트와 출력 매개변수 리스트에 추가한다.
	    읽기 가능 소켓이 표준 입력인 경우 서버는 실행을 종료한다.
	    '''

    def run(self):
        inputs = [self.server, sys.stdin]
        self.outputs = []
        running = True
        while running:
            try:
                readable, writeable, exceptional = select.select(inputs, self.outputs, [])
            except select.error as e:
                break

            for sock in readable:
                if sock == self.server:
                    # handle the server socket
                    client, address = self.server.accept()
                    print('Chat server: got connection %d from %s'  % (client.fileno(), address))
                    # read the login name
                    cname = receive(client).split('NAME: ')[1]
                    # Computer client name and send back
                    self.clients += 1
                    send(client, 'CLIENT: ' + str(address[0]))
                    inputs.append(client)
                    self.clientmap[client] = (address, cname)
                    # Send joining information to other clients
                    msg = "\n(Connected: New client (%d) from %s)" % (self.clients, self.get_client_name(client))
                    for output in self.outputs:
                        send(output, msg)
                    self.outputs.append(client)
                elif sock == sys.stdin:
			        # handle standard input
                    junk = sys.stdin.readline()
                    running = False
                else:
			        # handle all other sockets
                    try:
                        data = receive(sock)
                        if data:
                            # send as new client's message...
                            msg = '\n#[' + self.get_client_name(sock) + ']>>' + data
                            # send data to all except ourself
                            for output in self.outputs:
                                if output != sock:
                                    send(output, msg)
                        else:
                            print("Chat server: %d hung up" % sock.fileno())
                            self.clients -= 1
                            sock.close()
                            inputs.remove(sock)
                            self.outputs.remove(sock)
                            # sending client leaving information to others
                            msg = "\n(Now hung up: Client from %s)" % self.get_client_name(sock)
                            for output in self.outputs:
                                send(output, msg)
                    except socket.error as e:
                        # remove
                        inputs.remove(sock)
                        self.outputs.remove(sock)
        self.server.close()

'''
채팅 클라이언트는 name 인자를 초기화한 후, 채팅 서버 연결 시에 이 이름을 채팅 서버에 전송한다.
[name@hostname]> 형식의 프롬포트를 설정한다.
서버와 연결이 살아있는 동안  run() 메소드는 계속 작업을 수행한다.
sock의 값이 0이고 표준 입력에서 읽을 데이터가 있으면 데이터를 전송하고, 명령행 콘솔로 출력한다.
'''

class ChatClient(object):

    ''' A command line chat client using select '''
    def __init__(self, name, port, host=SERVER_HOST):
        self.name = name
        self.connected = False
        self.host = host
        self.port = port
        # Initial prompt
        self.prompt = '[' + '@'.join((name, socket.gethostname().split('.')[0])) + ']>'
        # Connect to server at port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, self.port))
            print("Now connected to chat server@ port %d" % self.port)
            self.connected = True
            # Send my name..
            send(self.sock, 'NAME: ' + self.name)
            data = receive(self.sock)
            # Contains client address, set it
            addr = data.split('CLIENT: ')[1]
            self.prompt = '[' + '@'.join((self.name, addr)) + ']> '
        except socket.error as e:
            print("Failed to connect to chat server @ port %d" % self.port)
            sys.exit(1)

    def run(self):
        ''' Chat client main loop '''
        while self.connected:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()
                # Wait for input from stdin and socket
                readable, writeable, exceptional = select.select([0, self.sock], [], [])
                for sock in readable:
                    if sock == 0:
                        data = sys.stdin.readline().strip()
                        if data: send(self.sock, data)
                    elif sock == self.sock:
                        data = receive(self.sock)
                        if not data:
                            print("Client shutting down.")
                            self.connected = False
                            break
                        else:
                            sys.stdout.write(data + '\n')
                            sys.stdout.flush()
            except KeyboardInterrupt:
                print("Client interrupted. ")
                self.sock.close()
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Socket Server Example with Select')
    parser.add_argument('--name', action='store', dest='name', required=True)
    parser.add_argument('--port', action='store', dest='port', type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    name = given_args.name
    if name == CHAT_SERVER_NAME:
	    server = ChatServer(port)
	    server.run()
    else:
	    client = ChatClient(name=name, port=port)
	    client.run()
