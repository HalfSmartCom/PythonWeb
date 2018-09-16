# 信号量
#
# 迷你唱吧
# 20个人，同一时间只能有四个人进去唱歌

from multiprocessing import Semaphore
from multiprocessing import Process
import time
import random


def sing(name, sema):
    sema.acquire()
    print("%s: entnter the ktv" % name)
    time.sleep(random.randint(1, 10))
    print("%s: leave the ktv" %name)
    sema.release()


if __name__ == "__main__":
    sema = Semaphore(4)
    for i in range(20):
        p = Process(target=sing, args=(i, sema))
        p.start()
