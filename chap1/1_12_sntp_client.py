import socket
import struct
import sys
import time

# 클라이언트 프로그램이 접속할 NTP 서버의 주소
NTP_SERVER = "0.uk.pool.ntp.org"
# 기준 시간인 1970년 1월 1일
TIME1970 = '2208988800L'

def sntp_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # SNTP 프로토콜 데이터
    data = '\x1b' + 47 * '\0'
    # sendto, recvfrom은 UDP 클라이언트 프로그램 메서드
    client.sendto(data, (NTP_SERVER, 123))
    data, address =  client.recvfrom (1024)
    if data:
        print("Response received from: ", address)
    # 서버가 시간 정보를 패킹한 배열을 담아 반환하면
    # 클라이언트는 struct 모듈을 사용해 언팩한다.
    t = struct.unpack('!12I', data)[10]
    # 실제 현재 시간을 얻으려먼 언팩한 데이터로부터 기준 시간 TIME1970을 빼야한다.
    t -= TIME1970
    print('\tTime=%s' % time.ctime(t))

if __name__ == "__main__":
    sntp_client()
