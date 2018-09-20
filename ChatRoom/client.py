import socket
import time
import struct
import json

ip_port = ("127.0.0.1", 9999)

class ChatClient:
    def __init__(self, username):
        self.username = username
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建TCP 对象
        self.socket.connect(ip_port)                                    # 连接server
        self.package = {                   # 一个package信息
            "msg" : None,
            "name" : self.username,
        }

    def send_msg(self, msg):
        self.package["msg"] = msg            # update 字典中的信息
        j_msg = json.dumps(self.package)     # 将字典转换为json 格式
        byte_length = struct.pack("i", len(j_msg)) # 计算字典的长度，并以编码为固定长度
        self.socket.send(byte_length)              # 发送json 的长度
        self.socket.send(j_msg.encode("utf-8"))   # 发送数据

    def recv_msg(self):
        info_length = self.socket.recv(4)              # 接收 server端的信息, 先接受数据长度
        data_length = struct.unpack("i", info_length)[0] # 解码，转换为数据长度
        data = self.socket.recv(data_length).decode("utf-8")            # 接收一个package
        return ("【机器人小图】"+" "+time.strftime('%Y-%m-%d:%H:%M:%S',time.localtime(time.time())) + "\n"+ data)


    def main(self):
        data = self.socket.recv(1024).decode("utf-8")  # 接收问好信息
        print(data)
        while True:
            msg=input("我：")
            if msg == "exit":
                print("聊天室已关闭")
                break
            self.send_msg(msg)
            msg = self.recv_msg()
            print(msg)


if __name__ == '__main__':
    client = ChatClient(username="小明")
    client.main()