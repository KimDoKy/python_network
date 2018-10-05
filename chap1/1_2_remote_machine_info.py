import socket

def get_remote_machine_info():
    remote_host = 'www.naver.com'
    try:
        print("IP address of %s: %s" % (remote_host, socket.gethostbyname(remote_host)))
    except socket.error as e:
        print(f'{remote_host}', ": ", f'{e}')

if __name__ == '__main__':
    get_remote_machine_info()
