# from multiprocessing import Process
# import time
#
#
# def fun():
#     print("aaa")
#     time.sleep(5)
#     print("bbb")
#
#
# if __name__ == "__main__":
#     p = Process(target=fun)
#     p.start()
#     print(p.is_alive())
#     time.sleep(0.1)
#     p.terminate()

# 属性
# pid 查看进程的pid
# name 查看进程的名字


from multiprocessing import Process
import time


class MyProcess(Process):
    def run(self):
        print("aaa name = %s, pid = %s", (self.name, self.pid))


if __name__ == "__main__":
    p = MyProcess()
    p.start()
    print(p.pid)
    print(p.name)
