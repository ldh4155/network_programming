from tkinter import *
from socket import *
import threading
import struct

#섭씨 온도를 서버로 전송
def calculate():
    global temp
    temp = float(entry1.get())
    sock.send(str(temp).encode())

def handler(sock):
    while True:
        try:
            r_msg = sock.recv(1024)
        except:
            pass
        else:
            entry2.delete(0,END)
            entry2.insert(0,r_msg.decode())

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(("localhost",2500))

root = Tk()
message_label = Label(text="Enter a temperature(C) ", font=('Verdana',16))
entry1 = Entry(font=('Verdana',16),width=5)

recv_label = Label(text="Temperature in F  ", font=('Verdana',16))
entry2 = Entry(font=('Verdana',16),width=5)

calc_button = Button(text='전송', font=('Verdana',12), command=calculate)

message_label.grid(row=0, column=0, sticky=W)
recv_label.grid(row=1, column=0, sticky=W)
entry1.grid(row=0, column=1)
entry2.grid(row=0, column=1)
calc_button.grid(row=0, column=2, padx=10, pady=10)

cThread = threading.Thread(target=handler, args=(sock,))
cThread.daemon = True
cThread.start()

root.mainloop()