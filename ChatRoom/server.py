import socket
import time
import threading
import requests
import json
import struct

ip_port = ("127.0.0.1", 9999)

class ChatServer:
    def __init__(self, key):
        # 绑定服务器的ip和端口，注意以tuple的形式
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(ip_port)
        self.socket.listen()
        # 图灵机器人，授权码
        self.key = key  # 存上你自己的key
        print("正在监听 127.0.0.1 ：{}...".format(ip_port[1]))

    def recive(self, conn):
        msg = conn.recv(4)
        json_length = struct.unpack("i", msg)[0]  # 获取数据包长度，避免粘包
        json_data = conn.recv(json_length)
        return json.loads(json_data)

    def send_msg(self, conn, msg):
        msg = msg.encode("utf-8")
        msg_length = struct.pack("i", len(msg))
        conn.send(msg_length)
        conn.send(msg)

    def tcplink(self, conn, addr):
        # 每次连接，开始聊天前，先欢迎下。
        conn.send("你好，欢迎来到机器人聊天器！".encode("utf-8"))
        while True:
            try:
                json_data = self.recive(conn)
                msg = json_data["msg"]
                name = json_data["name"]
                print("【"+name+"】 "+time.strftime('%Y-%m-%d:%H:%M:%S',time.localtime(time.time())))
                print(msg)
                response = self.get_response(msg)
                self.send_msg(conn, response)
            except:
                conn.close()
                print("与 {} 结束聊天！".format(name))
                break

    def get_response(self, info):
        # 调用图灵机器人API
        url = 'http://www.tuling123.com/openapi/api?key=' + self.key + '&info=' + info
        res = requests.get(url)
        res.encoding = 'utf-8'
        jd = json.loads(res.text)
        return jd['text']

    def main(self):
        while True:
            conn, addr = self.socket.accept()
            t = threading.Thread(target=self.tcplink, args=(conn, addr))
            t.start()


if __name__ == '__main__':
    with open("key") as f:
        key = f.read()
    cs = ChatServer(key=key)
    cs.main()