from multiprocessing import Pipe
from multiprocessing import Process


def fun(p):
    foo, son = p
    foo.close()
    # while True:
    #     try:


if __name__ == "__main__":
    foo, son = Pipe()
    p = Process(target= fun, args=((foo, son), ))

