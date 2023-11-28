from socket import *
from  tkinter import *
from select import *
import time

root = Tk() #기본 윈도우 생성
btn_color = 'red' #버튼 색상
btn_text = 'ON' #버튼 텍스트

def button_command():
    global sock, btn_text, btn_color
    if btn_text == 'ON':
        btn_text = 'OFF'
        btn_color = 'blue'
    else:
        btn_text = 'ON'
        btn_color = 'red'
    LED_button.configure(text=btn_text, bg=btn_color)
    sock.send(btn_text.encode())

def handle():
    global root, sock, switch_label, sock_list
    #root.mainloop()
    r_sock, w_sock, e_sock = select([sock], [], [], 0)
    if r_sock:
        msg = sock.recv(1024).decode()
        print(msg)
        if msg.upper() == 'OFF':
            switch_state_label.configure(text='Switch is OFF')
        else:
            switch_state_label.configure(text='Switch is ON')
    root.after(200, handle)


LED_label = Label(text="LED")
switch_label = Label(text="SWITCH")
switch_state_label = Label(text="Switch is OFF", fg='blue')
LED_button = Button(text=btn_text, fg='yellow', bg=btn_color, command=button_command)

#위젯 배치
LED_label.grid(row=0, column=0)
LED_button.grid(row=0, column=1)
switch_label.grid(row=1, column=0)
switch_state_label.grid(row=1, column=0, sticky=E)

#소켓 생성후 서버로 연결
sock = socket()
sock.connect(('localhost',2500))
mainloop()

