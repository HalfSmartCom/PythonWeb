# 例子
# 请求网页
    # 网页延时 IO 操作
# 单进程
    # 10个页面，同时访问多个
    # 分析页面

import requests
import os
from multiprocessing import Pool



def get_pages(url):
    print("进程%s get %s" %(os.getpid(), url))
    response = requests.get(url)
    if response.status_code == 200:
        return {"url":url, "text": response.text}

def parse_page(res):
    print("进程%s parse %s" % (os.getpid(), res['url']))
    parse_res = 'url:<%s> size:[%s]\n' %(res['url'],len(res['text']))
    with open("db.text", 'a') as f:
        f.write(parse_res)

if __name__ == "__main__":
    urls = [
        'https://www.baidu.com',
        'https://www.python.org',
        'https://www.openstack.org',
        'https://help.github.com/',
        'http://www.sina.com.cn/'
    ]

    p = Pool(3)
    res_l = []
    for url in urls:
        res = p.apply_async(get_pages, args=(url,), callback = parse_page )
        res_l.append(res)
    p.close()
    p.join()
    print([res.get() for res in res_l])

