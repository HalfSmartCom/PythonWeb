import time
import os
from multiprocessing import Pool


def func(i):
    time.sleep(1)
    i += 1
    print(i,os.getpid())
    return i + 1


if __name__ == "__main__":
    p = Pool(10)
    res_l = []
    for i in range(20):
        # p.apply(func, args=(i, ))
        res = p.apply_async(func, args=(i, ))
        res_l.append(res)

    p.close() # 不允许添加新的任务了
    p.join()
    for i in res_l:
        print(i.get())