import socketserver


class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        info = self.request.recv(1024).decode("utf-8")
        print(info)
        msg = input(">>>")
        self.request.send(msg.encode("utf-8"))


if __name__ == "__main__":
    server = socketserver.TCPServer(("127.0.0.1", 9999), MyServer)
    server.serve_forever()
