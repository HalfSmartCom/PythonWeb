# Manager 是一个类，就提供了可以进行数据共享的一个机制，
# 提供了很多数据类型 dict list pipe ,
# 不提供数据安全
import time
from multiprocessing import Manager
from multiprocessing import Process


def func(dic):
    while True:
        print(dic)
        time.sleep(3)


if __name__ == "__main__":
    m = Manager()
    dic = m.dict({"count": 100})
    p = Process(target=func, args=(dic, ))
    p.start()
    # p.join()