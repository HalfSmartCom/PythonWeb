
from multiprocessing import Queue
from multiprocessing import Process
# import time
# import random

def producer(q, food):
    for i in range(100):
        # time.sleep(0.1)
        procuct = "第%d-%s"%(i, food)
        print("产生", procuct)
        q.put(procuct)


def consumer(q, name):
    for i in range(100):
        print("%s吃 %s" %(name, q.get()) )
        # time.sleep(random.random())


if __name__ == "__main__":
    q = Queue(20)
    p1 = Process(target=producer, args=(q,"包子"))
    p1.start()
    p2 = Process(target=producer, args=(q, "馒头"))
    p2.start()
    c1 = Process(target=consumer, args=(q,"alex"))
    c1.start()
    # c2 = Process(target=consumer, args=(q, "jack"))
    # c2.start()


    
# 队列不会不安全