# 创建命令行窗口的进度条
# 实现刷新进度条可以不用换行，每次将光标移动到行首
import sys
import time


class ProcessBar(object):
    def __init__(self, total):
        self.total = total

    def process_bar(self, num):
        percent = num * 100 // self.total
        if num < self.total:
            sys.stdout.write("=" * percent + ">" + str(percent) + "%" + "\r")
        else:
            percent = 100
            sys.stdout.write("=" * percent + ">" + str(percent) + "%" + "\n")
        sys.stdout.flush


if __name__ == "__main__":
    processBar = ProcessBar(1000)
    num = 10
    while num <= 1000:
        processBar.process_bar(num)
        num += 10
        time.sleep(0.1)

