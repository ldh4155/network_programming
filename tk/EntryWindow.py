from tkinter import *

def calc(event):
    label.config(text="계산결과: " + str(eval(entry.get())))

root = Tk() #TK instance 생성

label = Label(root, text="0") #label 생성
label.pack() #레이블을 화면에 배치

entry = Entry(root, width=30)
entry.bind("<Return>", calc) #이벤트 부여
entry.pack()
root.mainloop() #TK화며 호출