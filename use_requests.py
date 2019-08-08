import requests
import json
def get_book():
    """ 获取书的信息 """
    url = 'http://search.dangdang.com/'
    rest = requests.get(url,params={
        'key': '9787115428028',
        'act': 'input'
    })
    print(rest.text)
    # json的方式获取数据
    # print(rest.json())
    print(rest.status_code)
    print(rest.encoding)

    #HTTP状态码
    # 200 2X开头说明请求成功
    # 4X开头说明请求失败
    # 500 服务器正忙


if __name__ == '__main__':
    get_book()