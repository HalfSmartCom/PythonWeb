from multiprocessing import JoinableQueue
from multiprocessing import Process
import time
import random
# put
# get 处理数据 task_done 消费结束


def producer(q, food):
    for i in range(10):
        # time.sleep(0.1)
        procuct = "第%d-%s"%(i, food)
        print("产生", procuct)
        q.put(procuct)
        time.sleep(random.randint(1,4))
    q.join()


def consumer(q, name):
    while True:
        food = q.get()
        print("%s 吃了 %s" %(name, food))
        q.task_done()


if __name__ == "__main__":

    q = JoinableQueue()
    p1 = Process(target=producer, args=(q, "包子"))
    p1.start()
    p2 = Process(target=producer, args=(q, "馒头"))
    p2.start()
    c1 = Process(target=consumer, args=(q, "alex"))
    c1.daemon = True
    c1.start()
    c2 = Process(target=consumer, args=(q, "jack"))
    c2.daemon = True
    c2.start()

    c3 = Process(target=consumer, args=(q, "mike"))
    c3.daemon = True
    c3.start()

    p1.join()
    p2.join()
