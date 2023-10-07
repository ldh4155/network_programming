import socket

port = 2500
BUFFSIZE = 1024
#소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", port))

while True:
    data, addr = sock.recvfrom(BUFFSIZE) #메시지 수신
    print("Recevied message: ", data.decode())
    resp = input(":")
    sock.sendto(resp.encode(),addr)