import requests
import re
import json

def spider(sn , book_list=[]):
    """爬取淘宝网的数据"""
    url = 'https://s.taobao.com/search?q={0}'.format(sn)
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
               'cookie': 't=9143d13cbbe0d30b6979e0271f233d00; tg=0; miid=662008151389073327; thw=cn; v=0; cookie2=1b544cb456903af70b38541027a6098f; _tb_token_=53e73a7e8eb3e; cna=YcN+FYfK8UYCAd9IWD7tvT4S; hng=CN%7Czh-CN%7CCNY%7C156; unb=2268312413; uc3=nk2=F4%2Bi%2BemBX8LqpA%3D%3D&vt3=F8dBy32v%2B6w4uo55uDw%3D&lg2=URm48syIIVrSKA%3D%3D&id2=UUpngHjGmrbDQg%3D%3D; csg=e5c91112; lgc=tyut%5Cu5F20%5Cu7FBD%5Cu5EB7; cookie17=UUpngHjGmrbDQg%3D%3D; dnk=tyut%5Cu5F20%5Cu7FBD%5Cu5EB7; skt=83c83238e73a1b09; existShop=MTU2NTM2ODA3OQ%3D%3D; uc4=id4=0%40U2gtEbc6fpLw%2F2ZDvwt3rmumR6Fn&nk4=0%40FZUT6mSOAUUG62Os7RZYcjt4Az9r; tracknick=tyut%5Cu5F20%5Cu7FBD%5Cu5EB7; _cc_=VFC%2FuZ9ajQ%3D%3D; _l_g_=Ug%3D%3D; sg=%E5%BA%B730; _nk_=tyut%5Cu5F20%5Cu7FBD%5Cu5EB7; cookie1=VAcMMRkzo64HOicc39TEl9JcydIIg12iZlxS39CEQBM%3D; enc=8KnzVOSFBOj5kFc4ff%2BqySF42os%2BodUqJZIjsyhJqXcAk5tbMFthH5FonIIeqDZxVpgpmlPRj7uaDXmP7kSNUA%3D%3D; mt=ci=109_1; swfstore=250583; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; JSESSIONID=0080FAB76287DF15537EDB02E8AA5FF0; l=cBrj_chrqRUmYFTDKOCNNuI8UUQODIRAguPRwdDJi_5LY68_ol7OkWt3pFJ6cjWdtGYB4s6vWje9-etuiqa0mGt-g3fP.; isg=BKCgG2Tr6a50rFWqVMvJ8oxdca6yAYbF2pwPmBqx7LtOFUA_wrm0A2Gnrf0wpTxL; uc1=cookie14=UoTaHY1ZOjMqtg%3D%3D&lng=zh_CN&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&existShop=false&cookie21=VT5L2FSpccLuJBreK%2BBd&tag=8&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&pas=0; whl=-1%260%260%261565369042527'}
    #获取html内容
    text = requests.get(url, headers=headers).text
    print(text)
    p = re.compile(r'g_page_config = (\{.+\});\s*', re.M)
    rest = p.search(text)
    print(rest)
    if rest:
        print(rest.group(1))
        data = json.loads(rest.group(1))
        bk_list = data['mods']['itemlist']['data']['auctions']

        print(len(bk_list))
        for bk in bk_list:
            # 标题
            title = bk["raw_title"]
            print(title)
            # 价格
            price = bk["view_price"]
            print(price)
            # 购买链接
            link = bk["detail_url"]
            print(link)
            # 商家
            store = bk["nick"]
            print(store)
            book_list.append({'title': title, 'price': price, 'link': link, 'store': store})
            print('{title}:{price}:{link}:{store}'.format(title=title, price=price, link=link, store=store))
            book_list.append({
                'title': title,
                'price': price,
                'link': link,
                'store': store
            })
            print('------------------------')

if __name__ == '__main__':
    spider('9787115428028')