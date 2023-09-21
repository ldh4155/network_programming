import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
address = ('', 5000)
s.bind(address)
s.listen(5)

client, addr = s.accept()

while True:
    time.sleep(1)

    print("Connection requested from", addr)
    client.send(time.ctime(time.time()).encode())

