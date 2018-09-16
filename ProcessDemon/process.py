# 多进程练习
# 开启多个子进程

# from multiprocessing import Process
# import os
# # import time
#
#
# def fun(name):
#     print("subprocess is %d and pid is %d, the parent pid is %d" % (name, os.getpid(), os.getppid()))
#
#
# if __name__ == "__main__":
#     print("parent pid is %d" % os.getpid())
#     p_lst = []
#     for i in range(50):
#         p = Process(target=fun, args=(i,))
#         p.start()
#         p_lst.append(p)
#     for p in p_lst:
#         p.join()
#     print("父进程结束")
#     # time.sleep(4)


from multiprocessing import Process
import os


class MyProcess(Process):
    def __init__(self, arg1):
        super().__init__()
        self.arg1 = arg1

    def run(self):
        while True:
            print("子进程： %s, arg1 = %s" % (os.getpid(), self.arg1))


if __name__ == "__main__":
    p = MyProcess(100)
    p.daemon = True
    p.start()
    print("主进程：%s" % os.getppid())