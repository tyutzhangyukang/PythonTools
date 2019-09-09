
import requests
from lxml import html

def spider(sn,book_list=[]):
    """爬取京东的图书数据"""
    url = 'https://search.jd.com/Search?keyword={0}'.format(sn)
    #获取HTML文档
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'cookie': 'shshshfpa=f1985da4-ef31-c975-d8f4-2f97565190eb-1559747216; shshshfpb=ebPN0t5shze0izHhROpfoxA%3D%3D; __jdv=76161171|direct|-|none|-|1564913170746; PCSYCityID=CN_110000_110100_110108; areaId=1; user-key=f438d62c-cfb9-4d38-a031-c6d3e08ba29c; cn=0; TrackID=1UrPhbi7R06wW6KxVZYRn7-EEhCQth-kH2g7eIpJiV6ht7ytFATA3vaZszrDRS5icn5VJEv11vaf1P8cRp1-EDDybAhh-zm8x78686v_sp-c; pinId=iYoV7eyy7ePHEFTa8EhSYw; pin=tyutzhangyukang; unick=tyutzhangyukang; _tp=RaDZM2a2obe%2F8YzOWMmZ1Q%3D%3D; _pst=tyutzhangyukang; xtest=3763.cf6b6759; ipLoc-djd=1-2810-51081-0.499187512; ipLocation=%u5317%u4eac; __jdu=15597472160601646818670; __jda=122270672.15597472160601646818670.1559747216.1564913171.1565408281.3; __jdb=122270672.2.15597472160601646818670|3.1565408281; __jdc=122270672; shshshfp=17f98def5b4fcd58a5783ac34f2fe5d9; shshshsID=a5c1895342588070d98776eb180c6838_2_1565408286811; qrsc=3; rkv=V0500; 3AB9D23F7A4B3C9B=3DGNECV7CPWKFSNUYWYI2XQO3RZ4FIAYCHOVXL6R5RH7VADFNA5YCSLEFW2DHYG4ZINSUTINDLCKI5FLK47DUKN7PY'}

    # 获取html内容
    resp  = requests.get(url, headers=headers)
    print(resp.encoding)
    resp.encoding = 'utf-8'
    html_doc = resp.text
    #获取xpath对象
    selector = html.fromstring(html_doc)
    print(len(selector))
    #找到列表的集合
    li_list = selector.xpath('//div[@id="J_goodsList"]/ul/li')
    print(len(li_list))
    #解析对应的内容，标题，价格，链接
    for li in li_list[ 25:]:
        #标题
        title = li.xpath('div/div[@class="p-name"]/a/@title')
        print(title[0])
        #购买链接
        link = li.xpath('div/div[@class="p-name"]/a/@href')
        print(link[0])
        #价格
        price = li.xpath('div/div[@class="p-price"]/strong/i/text()')
        print(price[0])
        #店铺
        store = li.xpath('div//div[@class="p-shopnum"]/a/@title')
        #store = li.xpath('div//a[@class="curr-shop hd-shopname"]/@title')
        store = '京东自营' if len(store) == 0  else store[0]
        print(store)
        book_list.append({
            'title': title[0],
            'price': price[0],
            'link': link[0],
            'store': store[0]
        })
        print('------------------')

if __name__ == '__main__':
    spider('9787115428028')