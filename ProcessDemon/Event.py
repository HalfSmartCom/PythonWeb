# 事件 -- 异步阻塞
# 事件 标志 同时 使所有进程陷入阻塞

# 红绿灯


from multiprocessing import Event
from multiprocessing import Process
import random
import time

def traffic_light(e):
    while True:
        if e.is_set():
            print("红灯")
            time.sleep(3)
            e.clear()  # 清除 阻塞
        else:
            print("绿灯")
            time.sleep(3)
            e.set()  # 设置阻塞


def car(e, name):
    e.wait()
    print("%i车通过" % name)


if __name__ == "__main__":
    e = Event() # 实例化一个事件
    p = Process(target=traffic_light, args=(e,)) # 创建一个交通灯进程
    p.start()
    for i in range(100):
        if i % random.randint(1, 20) == 0:
            time.sleep(random.randint(1,3))
        car_process = Process(target=car, args=(e, i))
        car_process.start()


