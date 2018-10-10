### 자신의 컴퓨터 이름과 IPv4 주소 출력
자신의 컴퓨터 정보를 얻는 방법
1_1_local_machine_info

### 외부 컴퓨터의 IP 주소 가져오기
외부 컴퓨터의 IP주소를 얻는 방법
1_2_remote_machine_info
`gethostbyname()`은 외부 컴퓨터의 IP 주소를 알아낼때 사용한다.

### IPv4 주소를 다른 포맷으로 변환
ip4_address_conversion 함수
1_3_ip4_address_conversion
binascii 모듈의 `hexlify` 함수는 바이너리 데이터를 16진수 포맷으로 표현할 때 사용한다.

### 주어진 포트 번호와 프로토콜 정보로 서비스 이름 찾기
find_service_name 함수
1_4_finding_service_name
`getservbyport()`를 이용해 서비스 이름을 알아낼 수 있다.

### 호스트 컴퓨터와 네트워크 바이트 순서에 맞게 정수를 변환하기
파이썬의 소켓 라이브러리의 `ntohl()`과 `htonl()` 함수는 네트워크 바이트 순서를 호스트가 사용하는 바이트 순서로 변환하거나 역으로 호스트의 바이트 순서로 네트워크 바이트 순서로 변환한다.
n은 network, h는 host, l은 long, s는 short를 의미함.

1_5_interger_conversion

### 기본 소켓 타임아웃 값을 설정하거나 얻기
소켓 객체를 생성한 후, `gettimeout()` 메소드로 기본 타임아웃 값을 얻고, `settimeout()` 메소드로 새로운 타임아웃 값을 설정할 수 있다.
`settimeout()`의 매개변수의 값은 초 단뒤의 음수가 아닌 실수이거나 None이 될 수 있다.

### 소켓 에러를 간결하면서도 자연스럽게 처리하기
`sendall()`의 argument가 교재에서는 str으로 되어 있지만, 버전의 차이로 판단되는 문제로 바이트로 입력을 요청하고 있는 에러가 있다. 현재 집에 인터넷이 안되어서, 추후 해당 문제 해결 예정

```python
message = "GET %s HTTP/1.0\r\n\r\n" % filename
s.sendall(message.encode())
```
인코딩처리하여 해결.

하지만, 새로운 에러 등장.(윈도우환경)
```
소켓이 연결되어 있지 않거나 sendto 호출을 사용하여 데이터그램 소켓에 보내는 경우에 주소가 제공되지 않아서 데이터를 보내거나 받도록 요청할 수 없습니다
```
리눅스에서 재 시도 예정.

### 소켓의 전송/수신 버퍼 크기 변경
`setsockopt()` 메소드로 기본 소켓 버퍼 크기를 변경한다.
`SEND_BUF_SIZE`와 `RECV_BUF_SIZE` 두 상수를 정의하여 소켓 객체의 `setsockopt()` 메소드를 호출한다.
`setsockopt()` 메소드는 `level`, `optname`(옵션이름), `value`(옵션에 대응하는 실제 값)라는 3개의 인자를 받는다.
`level`에 필요한 상수는 socket 모듈에서 찾을 수 있다.

### 소켓의 블로킹/논블로킹 모드 변경

### 소켓 주소 재사용

### 인터넷 시간 서버로부터 현재 시간을 얻은 후 출력

### SNTP 클라이언트 작성

### 간단한 에코 클라이언트/서버 애플리케이션 작성
