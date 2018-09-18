# 爬取西刺免费代理
# 获取页面上的ip地址以及端口号
# 验证代理ip是否有效
# 目前只实现了主页面的爬取
# 自己维护一个ip池

import requests
import re
import json

ip_pattern =re.compile( r'<tr class="odd">.*?<td>(?P<ip>.*?)</td>.*?<td>(?P<port>.*?)</td>.*?<td>(?P<address>.*?)</td>.*?<td>(?P<type>.*?)</td>.*?</tr>', re.S)

def parse_page(text):   # 获取页面的有效信息
    res = ip_pattern.finditer(text)
    for item in res:
        yield {
            "ip" : item.group("ip"),
            "port": item.group("port"),
            "address": item.group("address"),
            "type": item.group("type"),
        }


def check_valuable(ips):
    for ip in ips:
        proxies = {ip["type"]:ip["ip"]+":"+ip["port"]}
        try:
            requests.get("http://www.baidu.com", proxies = proxies)
            yield proxies
        except:
            print("无效的ip", proxies)
            continue

if __name__=="__main__":
    # url = "http://www.xicidaili.com/"
    base_url = "http://www.xicidaili.com/nn/"
    urls = [base_url + str(i) for i in range(1, 100)]
    headers = {
    	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
		"Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
		"Cache-Control": "max-age=0",
		"Connection": "keep-alive",
        # "Cookie": "_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWNlYjA5NWZhYWYwOTg1ZTkwMWNhNTBkYWNjMDg0ZjNkBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWQ1T25wdkc5MlMyWDdqTFQ3SjIybGFOa05YSTF6b3YzRERuN21xSWVGZWc9BjsARg%3D%3D--8aa1907a2496cdab214564009c6f1287ffa16717; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1536318216,1536318895,1537186043; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1537186043",
        "Host": "www.xicidaili.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    }
    f = open("ipPool.json", "w")
    for url in urls:
        html = requests.get(url, headers= headers).text
        items = parse_page(html)
        value_ips = check_valuable(items)
        for ip in value_ips:
            f.write(str(ip) + "\n")
            print(ip)
    f.close()


