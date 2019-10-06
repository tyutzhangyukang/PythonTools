import datetime
import json

import requests
from flask import Flask,redirect,request

app = Flask(__name__)

def get_ticket():
    url = 'https://api.weibo.com/oauth2/authorize?client_id=692588864&response_type=code&redirect_uri=http://www.computerzhang.cn'
    #get请求
    return url

def get_token(code):
    url = 'https://api.weibo.com/oauth2/access_token?client_id=692588864&client_secret=2500f50911ee6c93463a5d40f454e4aa&grant_type=authorization_code&redirect_uri=http://www.computerzhang.cn&code=' + code
    resp = requests.post(url)
    return resp.json()


def get_info(access_token, uid):
    url = 'https://api.weibo.com/2/users/show.json'
    resp = requests.get(url, {
        'access_token': access_token,
        'uid': uid
    })
    return resp.json()

def share(access_token):
    #分享数据，分享到微博
    url = 'https://api.weibo.com/2/statuses/share.json'
    resp = requests.post(url, {
        'access_token': access_token,
        'status': '现在是北京时间： {0} http://www.computerzhang.cn'.format(datetime.now())
    })
    return resp.json()


@app.route('/')
def index():
    code = request.args.get('code', None)
    #根据code获取token
    token = get_token(code)
    #获取用户信息
    user_info = get_info(token['access_token'],token['uid'])
    return json.dumps(user_info)

@app.route('/weibo')
def weibo():
    ticket = get_ticket()
    return redirect(ticket)

@app.route('/share')
def weibo():
    ticket = get_ticket()
    return redirect(ticket)

if __name__ == '__main__':
    # ticket = get_ticket()
    # print(ticket)
    app.run(debug=True,port=80)
