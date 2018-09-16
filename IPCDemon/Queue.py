# 进程之间的通信，

from multiprocessing import Queue
from multiprocessing import Process


def fun(q):
    print(q.get())


if __name__ == "__main__":
    q = Queue()
    q.put(100)
    p = Process(target=fun, args=(q,))
    p.start()


