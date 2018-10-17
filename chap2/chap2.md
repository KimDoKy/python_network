# chap2 | 더 나은 성능은 위한 소켓 I/O 멀티플렉싱

chap1 과 달리 여러 클라이언트가 서버에 동시에 접속해 비동기적으로 통신하는 상황을 다룬다. 즉, 각 클라이언트의 요구를 독립적으로 처리한다.
소켓 서버는 많은 클라이언트와 통신하는 상황을 염두해 두고 있기 때문에 `select` 모듈은 논블로킹 소켓을 감시하는데 매우 유용합니다.
`Diesel` 병렬 라이브러리로 클라이언트의 요구들을 동시에 처리한다.

> SocketServer -> socketserver | 파이썬 3.x으로 넘어가면서 모두 소문자로 변경되었다.
>

## 소켓 서버 애플리케이션에서 ForkingMixIN 사용
비동기적 소켓 서버 애플리케이션을 만든다면, 한 클라이언트의 요청을 기다리는 동안 블록 상태에 있으면 안된다.  
SocketServer 클래스의 ForkingMixIn 클래스는 각 클라이언트 연결 요청마다 새로운 프로세스를 생성한다.
ForkingServer 클래스가 에코 서버에서 직접 처리했던 소켓 생성, 주소 바인딩, 접속 요청 대기 같은 작업을 TCPServer 클래스가 알아서 처리한다.
ForkingServer는 클라이언트의 요청을 처리하는 방법을 지정하는 요청 핸들러를 설정하는데, 이 서버는 클라이언트로부터 받은 문자열을 다시 클라이언트에게 전송한다.
ForkingServer 클래스를 테스트하기 위해 여러 개의 에코 클라이언트를 띄우고 서버가 각 클라이언트와 어떻게 통신하는지 볼 수 있다.

2_1_forking_mixin_socket_server.py

## 소켓 서버 애플리케이션에서 ThreadingMixIn 사용

SocketServer 라이브러리를 사용해 비동기적인 네트워크 서버를 작성할 때 `ThreadingMixIn`으로 멀티스레드를 사용할 수 있다.
`ThreadedTCPServer`는 `TCPServer`, `ThreadingMixIn`으로부터 상속한다.
서버는 클라이언트가 연결하면 새로운 스레드를 생성한 후 실행한다.
`ForkingServerRequestHandler`는 스레드상에서 클라이언트가 전송한 데이터를 다시 클라이언트에게 전송한다. 클라이언트의 코드에서는 소켓을 생성 후 서버에 메시지를 전송한다.

2_2_threading_mixin_socket_server.py

서버 스레드를 생성한 후 백그라운드에서 실행한다. 그 후 3개의 테스트용 클라이언트를 생성한 후 각자 서버에 메시지를 전송한다.
서버 요청 핸들러의 handle() 메소드는 현재 스레드 정보를 탐색후 화면에 출력한다.
서버와 클라이언트 통신에서 모든 데이터를 손실 없이 전송하기 위해 `sendall()` 메소드를 사용한다.

## select.select를 이용한 채팅 서버 구현

`select`모듈의 `select()` 메소드를 사용하여 채팅 서버와 클라이언트 간의 전송과 수신 시 블록당하지 않으면서 모든 작업을 처리한다.

단일 스크립트로 클라이언트와 서버를 실행하되 매개변수를 이용해 서버와 클라이언트를 구분하는 예이다. 더 큰 큐모에서는 서버와 클라이언트를 별도의 모듈로 구현하는게 좋다.

> cPickle -> pickle 으로 변경되었다.

###  server

2_3_chat_server_with_select.py --name=server --port=8800

### client

2_3_chat_server_with_select.py --name=client1 --port=8800
2_3_chat_server_with_select.py --name=client2 --port=8800
