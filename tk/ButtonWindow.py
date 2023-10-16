from tkinter import *

count = 0

def count_plus():
    global count
    count += 1
    label.config(text=str(count))

def count_minus():
    global count
    count -= 1
    label.config(text=str(count))

root = Tk() #TK instance 생성

label = Label(root, text=count) #label 생성
label.pack() #레이블을 화면에 배치

button1 = Button(root, width=10, text="plus", overrelief="solid", command=count_plus)
button1.pack()

button2 = Button(root, width=10, text="minus", overrelief="solid", command=count_minus)
button2.pack()
root.mainloop() #TK화며 호출