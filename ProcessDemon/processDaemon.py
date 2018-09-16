# 报时器
# 子进程中每隔3s 报一次时间


import time
from multiprocessing import Process


def cal_time():
    while True:
        time.sleep(3)
        print("时间过去了3s")


if __name__ == "__main__":
    p = Process(target=cal_time)
    p.daemon = True
    p.start()
    for i in range(100):
        print('*' * i )
        time.sleep(0.5)


# 守护进程的进程的作用： 会随着主进程的代码执行结束而结束
# 守护进程 要在start之前设置
# 守护进程中，不能开机新的子进程
