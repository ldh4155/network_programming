import tkinter as tk
import threading
import cv2
import socket
import numpy as np
from PIL import Image, ImageTk
from UI import VideoChatUI

# 서버 IP 주소 및 포트 번호
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

# 웹캠 캡처를 위한 스레드
class VideoStreamThread(threading.Thread):
    def __init__(self, server_socket):
        super().__init__()
        self.server_socket = server_socket

    def run(self):
        cap = cv2.VideoCapture(0)  # 웹캠 캡처
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            _, img_encoded = cv2.imencode('.jpg', frame)
            img_bytes = img_encoded.tobytes()
            self.server_socket.sendall(img_bytes)


class VideoChatClient:
    def __init__(self):
        self.ui = VideoChatUI(tk.Tk(), "화상 채팅 클라이언트")
        self.ui.on_send_message = self.send_message_to_server

        # 클라이언트 소켓 설정
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER_IP, SERVER_PORT))

        # 비디오 수신 스레드 시작
        self.video_thread = threading.Thread(target=self.receive_video_stream)
        self.video_thread.daemon = True
        self.video_thread.start()

        # GUI 시작
        self.ui.window.mainloop()
    def show_frame(self):
        receive_frame_data = self.client_socket.recv(65536) #예상 최대 프레임
        receive_frame_array = np.frombuffer(receive_frame_data, dtype=np.uint8)
        receive_frame = cv2.imdecode(receive_frame_array, cv2.IMREAD_COLOR)
        if receive_frame is not None:
            self.ui.show_frame(receive_frame)
        self.ui.window.after(100, self.show_frame)

    def send_message_to_server(self, message):
        self.client_socket.send(message.encode())

    def send_message_to_clients(self, message):
        self.ui.receive_message(message) #클라이언트에서 받은 메시지를 UI에 표시

    def receive_message(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if not message:
                    break
                self.send_message_to_clients(message) #서버에서 받은 메시지를 UI에 표시
            except:
                pass

    # 서버로부터 비디오 스트리밍을 받아 화면에 표시하는 함수
    def receive_video_stream(self):
        while True:
            try:
                img_bytes = self.client_socket.recv(1024)
                img_encoded = np.frombuffer(img_bytes, dtype=np.uint8)
                frame = cv2.imdecode(img_encoded, cv2.IMREAD_COLOR)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            except Exception as e:
                print(e)
                break
            self.show_frame()
if __name__ == "__main__":
    client = VideoChatClient()


