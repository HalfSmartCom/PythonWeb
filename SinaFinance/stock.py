import requests
import time
import os
from lxml import etree
import random
import re
import json
from concurrent import futures

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
}
ip = {"type": "HTTPS", "ip": "116.77.205.32", "port": "80"}
def generateStockID():
    with open("stockpool", "r", encoding="utf-8")as f:
        stocknames = f.readlines()
    print(len(stocknames))
    for stockname in stocknames:
        try:
            stockid = re.search("\(([\d])+\)", stockname).group(0)
            yield stockid[1:-1]
        except AttributeError:
            pass

def generate_ip():
    with open("../IPPool/httpsPool1.json") as f:
        ips = f.readlines()
    return [json.loads(ip) for ip in ips]


class MyStock():
    def __init__(self, stock_id, year, season, ip_pool):
        self.stock_id = self.get_stock_id(stock_id)
        self.year = year
        self.season = season
        self.url = self.generate_url(self.stock_id, self.year, self.season)
        self.html = self.get_web_data(self.url, ip_pool)
        self.selector = etree.HTML(self.html)
        self.stock_data = []
        self.stock_name = None
        self.year_list = []
        try:
            self.stock_data = self.parse_page(self.selector)
            self.stock_name = self.get_stock_name(self.selector)
            self.year_list = self.get_valied_year(self.selector)
        except:
            pass

    def parse_page(self, selector):
        elements = selector.xpath('//tr/td/div/a/text()')
        data = selector.xpath('//tr/td/div/text()')
        result = []
        #  网页分为两种，分两种讨论
        # 前面的网页时间不是超链接， 在某一时间段之后，所有的时间都变成了超链接
        # 最后将每天的结果整个到一个List 中，供以后使用
        if len(elements) != 0:   # 分析时间是超链接的这种情况
            time_data = ",".join(elements).replace("\r", "").replace("\t", "").replace("\n", "").split(",")
            stock_data = ",".join(data).replace("\r", "").replace("\t", "").replace("\n", "").replace(",,", "").split(",")
            for i, item in enumerate(time_data):
                result.append([item] + stock_data[i * 6:(i + 1) * 6])
        else:                   # 时间不是超链接情况
            data = ",".join(data).replace("\r", "").replace("\t", "").replace("\n", "").split(",")
            temp = []            # 以下只是字符串处理
            for i, item in enumerate(data):
                if i != 0 and i % 7 == 0:    # 分组
                    result.append(list(temp))
                    temp.clear()
                temp.append(item)
        return result


    def generate_url(self, stock_id, year, season):
        url = "https://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s.phtml?year=%d=&jidu=%d" % (stock_id, year, season)
        return url


    def get_web_data(self, url, ip_pool):
        global ip
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "vip.stock.finance.sina.com.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        }
        proxies = {ip["type"]: ip["ip"] + ":" + ip["port"]}
        response = requests.get(url, headers=headers, proxies = proxies, timeout =10)
        if response.status_code == 200:
            print(proxies)
            return response.content.decode("gbk")
        else:
            print("正在切换ip......")
            ip = ip_pool[random.randint(0, len(ip_pool))]
            return self.get_web_data(url, ip_pool)

    def get_stock_id(self, num):
        base_id = '000000'
        stock_id = (base_id + str(num))[-6:]
        return stock_id

    def get_stock_name(html, selector):
        name_xpath = selector.xpath('//div[@class="tbtb01"]/h1/a/text()')
        id_xpath = selector.xpath('//div[@class="tbtb01"]/h2/text()')
        return name_xpath[0] + "(" + id_xpath[0].strip() + ")"

    def get_valied_year(self, selector):
        year_xpath = selector.xpath('//select[@name="year"]/option/text()')
        return year_xpath


def crawl_one_id(stock_id, ip_pool):
    # 爬取一支股票
    my_stock = MyStock(stock_id, 2018, 2, ip_pool)
    year_list = my_stock.year_list
    result = []
    if year_list == []:
        return (0, 0)
    for year in year_list:
        for season in range(4, 0, -1):
            my_stock = MyStock(stock_id, int(year), season, ip_pool)
            result.extend(my_stock.stock_data)
            print(my_stock.stock_name, year, season)
            # time.sleep(3)
    return (my_stock.stock_id, result)


def writeData2File(name, data):
    with open(r'D:\\stock_data\\' + name + ".csv", "w") as f:
        f.write(name + "\n")
        for item in data:
            f.write(",".join(item) + "\n")

def checkId():
    result = []
    path = 'D:\\stock_data\\'
    files = os.walk(path)
    for dirpath, dirnames, filenames in files:
        for filename in filenames:
            result.append(re.search("\d+", filename).group())
    return result


def main(id):
    try:
        name, data = crawl_one_id(id, ip_pool)
        if name != 0 and data != 0:
            writeData2File(name, data)
    except:
        print("pass")

if __name__ == "__main__":
    ip_pool = generate_ip()   # 在内存中产生一个IP池，所有的IP 都存在内存中，这个待改进
    id_exist = checkId()
    thread_pool = futures.ThreadPoolExecutor(20)
    f_lst = []
    for id in generateStockID():
        if id in id_exist:
            continue
        f = thread_pool.map(main, [id])
        f_lst.append(f)

