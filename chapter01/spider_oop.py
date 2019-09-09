import json
import re
from typing import NamedTuple

import requests
from lxml import html

class BootEntity(NamedTuple):
    """ 书本信息 """
    title: str
    price: float
    link: str
    store: str

    def  __str__(self):
        return '价格： {self.price} ; 名称： {self.title} ;  购买链接： {self.link} ; 店铺： {self.store}'.format(self=self)


class MySpider(object):
    def __init__(self, sn):
        self.sn = sn
        #存储所有的书本信息
        self.book_list = []

    def dangdang(self):
        """爬取当当网的数据"""
        url = 'http://search.dangdang.com/?key={sn}&act=input'.format(sn=self.sn)
        # 获取HTML内容
        html_data = requests.get(url).text
        # xpath对象
        selector = html.fromstring(html_data)
        # print(len(selector))
        ul_list = selector.xpath('//div[@id="search_nature_rg"]/ul/li')
        # print(len(ul_list))
        for li in ul_list:
            # 标题
            title = li.xpath('a/@title')
            # print(title[0])
            # 购买链接
            link = li.xpath('a/@href')
            # print(link[0])
            # 价格
            price = li.xpath('p[@class="price"]/span[@class="search_pre_price"]/text()')
            # print(price[0].replace('¥', ' '))
            # 商家
            store = li.xpath('p[@class="search_shangjia"]/a/text()')
            store = '当当自营' if len(store) == 0 else store[0]
            # print(store)
            book = BootEntity(
                title=title[0],
                price=price[0].replace('¥', ''),
                link=link[0],
                store=store
            )
            # print(book)
            self.book_list.append(book)


    def jd(self):
        """爬取京东的数据"""
        url = 'https://search.jd.com/Search?keyword={0}'.format(self.sn)
        # 获取HTML文档
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'cookie': 'shshshfpa=f1985da4-ef31-c975-d8f4-2f97565190eb-1559747216; shshshfpb=ebPN0t5shze0izHhROpfoxA%3D%3D; __jdv=76161171|direct|-|none|-|1564913170746; PCSYCityID=CN_110000_110100_110108; areaId=1; user-key=f438d62c-cfb9-4d38-a031-c6d3e08ba29c; cn=0; TrackID=1UrPhbi7R06wW6KxVZYRn7-EEhCQth-kH2g7eIpJiV6ht7ytFATA3vaZszrDRS5icn5VJEv11vaf1P8cRp1-EDDybAhh-zm8x78686v_sp-c; pinId=iYoV7eyy7ePHEFTa8EhSYw; pin=tyutzhangyukang; unick=tyutzhangyukang; _tp=RaDZM2a2obe%2F8YzOWMmZ1Q%3D%3D; _pst=tyutzhangyukang; xtest=3763.cf6b6759; ipLoc-djd=1-2810-51081-0.499187512; ipLocation=%u5317%u4eac; __jdu=15597472160601646818670; __jda=122270672.15597472160601646818670.1559747216.1564913171.1565408281.3; __jdb=122270672.2.15597472160601646818670|3.1565408281; __jdc=122270672; shshshfp=17f98def5b4fcd58a5783ac34f2fe5d9; shshshsID=a5c1895342588070d98776eb180c6838_2_1565408286811; qrsc=3; rkv=V0500; 3AB9D23F7A4B3C9B=3DGNECV7CPWKFSNUYWYI2XQO3RZ4FIAYCHOVXL6R5RH7VADFNA5YCSLEFW2DHYG4ZINSUTINDLCKI5FLK47DUKN7PY'}

        # 获取html内容
        resp = requests.get(url, headers=headers)
        # print(resp.encoding)
        resp.encoding = 'utf-8'
        html_doc = resp.text
        # 获取xpath对象
        selector = html.fromstring(html_doc)
        # print(len(selector))
        # 找到列表的集合
        li_list = selector.xpath('//div[@id="J_goodsList"]/ul/li')
        # print(len(li_list))
        # 解析对应的内容，标题，价格，链接
        for li in li_list:
            # 标题
            title = li.xpath('div/div[@class="p-name"]/a/@title')
            # print(title[0])
            # 购买链接
            link = li.xpath('div/div[@class="p-name"]/a/@href')
            # print(link[0])
            # 价格
            price = li.xpath('div/div[@class="p-price"]/strong/i/text()')
            # print(price[0])
            # 店铺
            store = li.xpath('div//div[@class="p-shopnum"]/a/@title')
            # store = li.xpath('div//a[@class="curr-shop hd-shopname"]/@title')
            store = '京东自营' if len(store) == 0 else store[0]
            # print(store)
            book = BootEntity(
                title=title[0],
                price=price[0],
                link=link[0].replace('//','http://'),
                store=store
            )
            # print(book)
            self.book_list.append(book)


    def taobao(self):
        """爬取淘宝的数据"""
        url = 'https://s.taobao.com/search?q={0}'.format(self.sn)
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'cookie': 't=9143d13cbbe0d30b6979e0271f233d00; tg=0; miid=662008151389073327; thw=cn; v=0; cookie2=1b544cb456903af70b38541027a6098f; _tb_token_=53e73a7e8eb3e; cna=YcN+FYfK8UYCAd9IWD7tvT4S; hng=CN%7Czh-CN%7CCNY%7C156; unb=2268312413; uc3=nk2=F4%2Bi%2BemBX8LqpA%3D%3D&vt3=F8dBy32v%2B6w4uo55uDw%3D&lg2=URm48syIIVrSKA%3D%3D&id2=UUpngHjGmrbDQg%3D%3D; csg=e5c91112; lgc=tyut%5Cu5F20%5Cu7FBD%5Cu5EB7; cookie17=UUpngHjGmrbDQg%3D%3D; dnk=tyut%5Cu5F20%5Cu7FBD%5Cu5EB7; skt=83c83238e73a1b09; existShop=MTU2NTM2ODA3OQ%3D%3D; uc4=id4=0%40U2gtEbc6fpLw%2F2ZDvwt3rmumR6Fn&nk4=0%40FZUT6mSOAUUG62Os7RZYcjt4Az9r; tracknick=tyut%5Cu5F20%5Cu7FBD%5Cu5EB7; _cc_=VFC%2FuZ9ajQ%3D%3D; _l_g_=Ug%3D%3D; sg=%E5%BA%B730; _nk_=tyut%5Cu5F20%5Cu7FBD%5Cu5EB7; cookie1=VAcMMRkzo64HOicc39TEl9JcydIIg12iZlxS39CEQBM%3D; enc=8KnzVOSFBOj5kFc4ff%2BqySF42os%2BodUqJZIjsyhJqXcAk5tbMFthH5FonIIeqDZxVpgpmlPRj7uaDXmP7kSNUA%3D%3D; mt=ci=109_1; swfstore=250583; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; JSESSIONID=0080FAB76287DF15537EDB02E8AA5FF0; l=cBrj_chrqRUmYFTDKOCNNuI8UUQODIRAguPRwdDJi_5LY68_ol7OkWt3pFJ6cjWdtGYB4s6vWje9-etuiqa0mGt-g3fP.; isg=BKCgG2Tr6a50rFWqVMvJ8oxdca6yAYbF2pwPmBqx7LtOFUA_wrm0A2Gnrf0wpTxL; uc1=cookie14=UoTaHY1ZOjMqtg%3D%3D&lng=zh_CN&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&existShop=false&cookie21=VT5L2FSpccLuJBreK%2BBd&tag=8&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&pas=0; whl=-1%260%260%261565369042527'}
        # 获取html内容
        text = requests.get(url, headers=headers).text
        # print(text)
        p = re.compile(r'g_page_config = (\{.+\});\s*', re.M)
        rest = p.search(text)
        # print(rest)
        if rest:
            # print(rest.group(1))
            data = json.loads(rest.group(1))
            bk_list = data['mods']['itemlist']['data']['auctions']

            # print(len(bk_list))
            for bk in bk_list:
                # 标题
                title = bk["raw_title"]
                # print(title)
                # 价格
                price = bk["view_price"]
                # print(price)
                # 购买链接
                link = bk["detail_url"]
                # print(link)
                # 商家
                store = bk["nick"]
                # print(store)

                book = BootEntity(
                    title = title,
                    price = price,
                    link = link.replace('//','http://'),
                    store = store
                )
                # print(book)
                self.book_list.append(book)
                # self.book_list.append({'title': title, 'price': price, 'link': link, 'store': store})
                # print('{title}:{price}:{link}:{store}'.format(title=title, price=price, link=link, store=store))
                # self.book_list.append({
                #     'title': title,
                #     'price': price,
                #     'link': link,
                #     'store': store
                # })

    def yhd(self):
        """爬取1号店的数据"""
        url = 'https://search.yhd.com/c0-0/k{0}/'.format(self.sn)
        # 获取到html对象
        html_doc = requests.get(url).text
        # xpath对象
        selector = html.fromstring(html_doc)
        # 书籍列表
        ul_list = selector.xpath('//div[@id="itemSearchList"]/div')
        #print(len(ul_list))
        # 解析数据
        for li in ul_list:
            # 标题
            # title = li.xpath('div//a[@class="mainTitle"]/@title')
            title = li.xpath('div//p[@class="proName clearfix"]/a/@title')
            # print(title[0])
            # 价格
            price = li.xpath('div//p[@class="proPrice"]/em/@yhdprice')
            # print(price[0])
            # 链接
            link = li.xpath('div//p[@class="proName clearfix"]/a/@href')
            # print(link[0].replace('//', 'http://'))
            # 店铺
            store = li.xpath('div//p[@class="searh_shop_storeName storeName limit_width"]/a/@title')
            # print(store[0])
            book = BootEntity(
                title = title[0],
                price = price[0],
                link = link[0].replace('//','http://'),
                store = store[0],
            )
            self.book_list.append(book)

    def spider(self):
        """得到排序后的数据"""
        self.dangdang()
        self.jd()
        self.yhd()
        self.taobao()
        bk_list = sorted(self.book_list, key=lambda item: float(item.price), reverse=True)
        for book in bk_list:
            print(book)


if __name__ == '__main__':
    client = MySpider('9787115428028')
    client.spider()