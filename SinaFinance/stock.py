import re
import requests
import time
from lxml import etree
from bs4 import BeautifulSoup


# my_url = "http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/000001.phtml?year=2011=&jidu=2"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
}
#
# titlePat = re.compile(r'(?<=strong>).*?(?=</strong>)')
# pricePat = re.compile(r'(?<="center">)[\s\d.-]*(?=</div>)', re.DOTALL)
# timePat = re.compile(r"<a target='_blank'.*?>.*?(?=</a>)", re.DOTALL)


class MyStock():
    def __init__(self, stock_id, year, season):
        self.stock_id = self.get_stock_id(stock_id)
        self.year = year
        self.season = season
        self.url = self.generate_url(self.stock_id, self.year, self.season)
        self.html = self.get_web_data(self.url)
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
        url = "http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s.phtml?year=%d=&jidu=%d" % (stock_id, year, season)
        return url

    def get_web_data(self, url):
        # text = requests.get(url, headers=headers, proxies = {'HTTPS': '114.225.170.140:53128'})
        # print(text.content.decode("utf-8"))
        content = requests.get(url, headers=headers, proxies={'HTTPS': '175.155.76.198:53128'}).content
        return content.decode("gbk")

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


def crawl_one_id(stock_id):
    my_stock = MyStock(stock_id, 2018, 2)
    year_list = my_stock.year_list
    result = []
    if year_list == []:
        return (0, 0)
    for year in year_list:
        for season in range(4, 0, -1):
            my_stock = MyStock(stock_id, int(year), season)
            result.extend(my_stock.stock_data)
            print(my_stock.stock_name)
            time.sleep(5)
    return (my_stock.stock_name, result)


if __name__ == "__main__":
    for id in range(600000, 700000):
        try:
            name, data = crawl_one_id(id)
            if name != 0 and data != 0:
                with open(r'D:\\stock_data\\'+ name + ".csv", "w") as f:
                    f.write(name + "\n")
                    for item in data:
                        f.write(",".join(item) + "\n")
        except:
            print("pass")
            pass




