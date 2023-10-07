import socket

port = 2500
BUFFSIZE = 1024
#소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    msg = input()
    sock.sendto(msg.encode(), ('localhost', port)) #메시지 송신
    data, addr = sock.recvfrom(BUFFSIZE) #메시지 수신
    print("Server says: ", data.decode())