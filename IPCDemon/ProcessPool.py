# 进程池
# 造一个池子，放4个进程来用来完成工作
# 发任务
# 使用池子中的进程完成任务

import os
import time
from multiprocessing import Pool

def func(i):
    i += 1
    print(i, os.getpid())


if __name__ == "__main__":
    p = Pool(10)
    p.map(func, range(20))
    p.close() # 不允许再向进程池中添加任务
    print("==>")
