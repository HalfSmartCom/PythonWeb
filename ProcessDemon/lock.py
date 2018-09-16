# 模拟抢票
# n个用户抢几张票


from multiprocessing import Lock
from multiprocessing import Process
import random
import time
import json


def search():
    with open("titck") as f:
        print(json.load(f)["count"])


def get(number):
    with open("titck") as f:
        titck_num = json.load(f)["count"]
    time.sleep(random.random())
    if titck_num > 0:
        with open("titck", 'w') as f:
            json.dump({"count":titck_num-1}, f)
        print("%s 买到票了" %number)
    else:
        print("%s 没买到票" %number)


def task(number, lock):
    search()
    lock.acquire()
    get(number)
    lock.release()


if __name__ == "__main__":
    lock = Lock()
    for i in range(20):
        p = Process(target=task, args=(i, lock))
        p.start()
