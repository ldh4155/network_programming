import cv2
import socket
import threading
from UI import VideoChatUI
import tkinter as tk
from PIL import Image, ImageTk

class VideoChatServer:
    def __init__(self):
        self.ui = VideoChatUI(tk.Tk(), "화상 채팅 서버")
        self.ui.on_send_message = self.send_message_to_clients
        self.clients = []

        #웹캠 초기화
        self.cap = cv2.VideoCapture(0)

        #소켓 초기화
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 12345))
        self.server_socket.listen(5)

        #웹캠 영상 전송 스레드 시작
        self.webcam_thread = threading.Thread(target=self.send_webcam)
        self.webcam_thread.daemon = True
        self.webcam_thread.start()

        #클라이언트 연결을 처리하는 스레드 시작
        self.receive_thread = threading.Thread(target=self.receive_clients)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        #서버 GUI 시작
        self.ui.window.mainloop()

    def show_frame(self, frame):
        self.ui.show_frame(frame)

    def send_message_to_clients(self, message):
        for client in self.clients:
            client.send(message.encode())
        #서버 UI에 메시지 표시
        self.ui.receive_message("서버: " + message)

    def send_message_to_server(self, message):
        self.ui.receive_message(message) #서버에서 받은 메시지를 UI에 표시
        self.send_message_to_clients(message) #받은 메시지를 다른 클라이언트에 전송

    def send_webcam(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue
            _, encoded_frame = cv2.imencode('.jpg', frame,
[int(cv2.IMWRITE_JPEG_QUALITY), 60])
            encoded_frame = encoded_frame.tobytes()
            for client in self.clients:
                try:
                    client.send(encoded_frame)
                except:
                    self.clients.remove(client)
            #서버 UI에 비디오 화면 표시
            self.show_frame(frame)
    def receive_clients(self):
        client_socket, client_address = self.server_socket.accept()
        self.clients.append(client_socket)
        while True:
            message = client_socket.recv(1024).decode()
            self.send_message_to_server(message)

    # 화면 갱신 함수
    def update(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.ui.label.config(image=photo)
            self.ui.label.image = photo
        self.ui.window.after(10, self.update)

    # 메시지 보내기 함수
    def send_message(self):
        message = self.ui.entry.get()
        self.ui.chat_text.config(state=tk.NORMAL)
        self.ui.chat_text.insert(tk.END, "나: " + message + "\n")
        self.ui.chat_text.config(state=tk.DISABLED)
        self.ui.entry.delete(0, tk.END)

server = VideoChatServer()
server.update()

