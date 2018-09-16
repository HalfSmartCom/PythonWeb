# 练习 super继承关系
#


class Base(object):

    def __init__(self):
        print("base init")

    def hello(self):
        raise NotImplemented


class Medium1(Base):
    def __init__(self):
        super(Medium1, self).__init__()
        print("medium1")

    def hello(self):
        print("Hello from Medium1")


class Medium2(Base):
    def __init__(self):
        super(Medium2, self).__init__()
        print("Medium2")

    def hello(self):
        print("Hello from Medium2")


class Leaf(Medium1, Medium2):
    def __init__(self):
        super(Leaf, self).__init__()
        print("leaf")

    def hello(self):
        Medium1().hello(self)
        Base().hello(self)
        print("Hello From Leaf")


if __name__ == "__main__":
    b = Base()
    m1 = Medium1()
    m2 = Medium2()
    l = Leaf()

    # b.hello()
    m1.hello()
    m2.hello()
    l.hello()

