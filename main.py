# coding: utf-8
import re
import requests
import time
from bs4 import BeautifulSoup

headers1 = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Ubuntu Chromium/44.0.2403.89 '
                         'Chrome/44.0.2403.89 '
                         'Safari/537.36'}

headers2 = {'authority': 'www.google.com',
            'method': 'GET',
            'path': '/client_204?cs=2',
            'scheme': 'https',
            'accept': '*/*',
            #'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': '1P_JAR=2021-07-02-06; '
                      'NID=218=k1cpDFcdSF9iOAckYvyT5VdG8dMMrbC4x0nBhgOv0MDtS65ET0DVBYfAWVYUunT1nV22haBQ4tsBuivzd6YUTtZcVP-n-LOuwzI00gRVzj1j1rePmIs6D3Md5QeqFVu2Jp-W3m7rhMlpvnmFtCreSJkfSDUfduzjUc1c1zxFOGE; '
                      'DV=M2WXnXAPMFolcNiZldgA7vxYtodeplc4dyRxmh2zaAIAAAA',
            'referer': 'https://www.google.com/',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'x-client-data': 'CJS2yQEIpLbJAQjBtskBCKmdygEIkv3KAQijoMsBCK3yywEI3PLLAQiP9MsBCIz4ywEItPjLAQie+csBGLryywEYkvXLAQ==',
            # 'Decoded':
            #             "message ClientVariations":{
            #                 'Active client experiment variation IDs.'
            #                 'repeated int32 variation_id = [3300116, 3300132, 3300161, 3313321, 3325586, 3330083, 3340589, 3340636, 3340815, 3341324, 3341364, 3341470];',
            #                 ' Active client experiment variation IDs that trigger server-side behavior.',
            #                 'repeated int32 trigger_variation_id = [3340602, 3340946];',
            #             }
            }


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Ubuntu Chromium/44.0.2403.89 '
                         'Chrome/44.0.2403.89 '
                         'Safari/537.36'}

domain = "https://www.google.com"

# 获取页面内容
def get_page(search_url):
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        return response.text
    except:
        return ""

# 处理页面内容
def get_blog_info(html):
    soup = BeautifulSoup(html, 'lxml')
    main_content = soup.find('div', attrs={'id': 'main'})
    # 处理搜索结果
    article_item = main_content.find_all('div', attrs={'class': 'ZINbbc xpd O9g5cc uUPGi'})
    for item in article_item:
        h3 = item.find('div', attrs={'class':'BNeawe UPmit AP7Wnd'})
        cat = h3.text
        link = item.find('div', attrs={'class':'kCrYT'})
        linkHref = link.a['href'].split("url?q=", -1)
        linkHrefDeal = linkHref[1].split("&sa=U&ved=", 1)
        title = item.find('div', attrs={'class':'BNeawe vvjwJb AP7Wnd'})
        titleCon = title.text
        desc = item.find('div', attrs={'class':'BNeawe s3v9rd AP7Wnd'})
        descCon = desc.text
        content = "from: " + cat + '\n' + "title: " + titleCon + '\n' + "link: " + linkHrefDeal[0] + '\n' + "content: " + descCon + '\n\n'
        now = time.strftime("%Y%m%d%H", time.localtime())
        write_to_file("search_result_"+now, "txt", content)
    # 分页连接获取及处理
    # next_link = main_content.find('div', attrs={'class':'nMymef MUxGbd lyLwlc'})
    # next_href = domain + next_link.a['href']
    # return next_href

# 写入文件
def write_to_file(filename, type, content):
    if "txt" == type:
        file = filename + '.txt'
        with open(file, 'a', encoding='utf-8') as f:
            f.write(content)
    else:
        file = filename + '.html'
        with open(file, 'a', encoding='utf-8') as f:
            f.write(content)
    f.close()
# 主函数
def main():
    # search_url = "https://www.google.com/search?q=everlane&sxsrf=ALeKk00-lBmwDg91HmKDxRmuzXfGEK20Cg:1625035491352&source=lnms&tbm=nws&sa=X&ved=2ahUKEwiKgtb54L7xAhWKwZQKHbM0AggQ_AUoA3oECAEQBQ&biw=1440&bih=695"
    # search_url = "https://www.google.com.hk/search?q=everlane&biw=1440&bih=695&tbm=nws&ei=4Y7eYOqyNJDO0PEPqMyOiAc&start=0&sa=N"
    start = 1260
    while start < 2000:
        search_url = f"https://www.google.com/search?q=everlane&biw=1440&bih=695&tbm=nws&ei=4Y7eYOqyNJDO0PEPqMyOiAc&start={start}&sa=N"
        html = get_page(search_url)   ## 根据连接抓取页面内容
        # print(html)
        write_to_file("search_res", "html", html)
        return
        if "" == html:
            write_to_file("search_urls", "txt", "\nstop here: " + search_url + "\n")
            break
        write_to_file("search_urls", "txt", "searched url: " + search_url + "\n")
        get_blog_info(html)    ## 处理抓取内容并返回下一页链接
        start += 10

if __name__ == '__main__':
    main()