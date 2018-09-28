import os
import re
import pandas as pd
import numpy as np
path = 'D:\\stock_data\\'
newPath = "D:\\stock_filter_data\\"
def checkId():
    result = []
    path = 'D:\\stock_data\\'
    files = os.walk(path)
    for dirpath, dirnames, filenames in files:
        for filename in filenames:
            yield  (filename, re.search("\d+", filename).group())


if __name__ == '__main__':
    for filename, id in checkId():
        print(filename)
        stock = pd.read_csv(path + filename, engine='python', encoding = "gbk", skiprows=1, index_col= 0, names=["data", "open", "high", "close", "low", "number", "volume"])
        stock = stock.sort_index(ascending=True)
        # stock["ma5"] = np.round(stock["close"].rolling(window=5, center=False).mean(), 2)
        # stock["ma10"] = np.round(stock["close"].rolling(window=10, center=False).mean(), 2)
        # stock["ma20"] = np.round(stock["close"].rolling(window=20, center=False).mean(), 2)
        stock.to_csv(newPath + id + ".csv")

