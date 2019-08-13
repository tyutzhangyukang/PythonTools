#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The Photon main part."""


from __future__ import print_function  # 这个语句是 Python2 的概念，Python3 相对于 Python2 是 future，在 Python2 的环境下超前使用 Python3 的 print 函数

import argparse  # 命令行参数解析
import os
import re
import sys
import time
import warnings  # 警告信息

import requests

from core.flash import flash
from core.prompt import prompt
from core.requester import requester
from core.config import intels
from core.zap import zap
from core.utils import top_level, extract_headers, is_link, entropy, regxy, remove_regex, timer, writer
from core.colors import bad, good, info, run, green, red, white, end

try:
    from urllib.parse import urlparse  # For Python 3，解析和组建url的函数
    python2, python3 = False, True
except ImportError:
    from urlparse import urlparse  # For Python 2
    python2, python3 = True, False


try:
    input = raw_input
except NameError:
    pass


# 打印 banner
print('''%s      ____  __          __
     / %s__%s \/ /_  ____  / /_____  ____
    / %s/_/%s / __ \/ %s__%s \/ __/ %s__%s \/ __ \\
   / ____/ / / / %s/_/%s / /_/ %s/_/%s / / / /
  /_/   /_/ /_/\____/\__/\____/_/ /_/ %sv1.2.1%s\n''' %
      (red, white, red, white, red, white, red, white, red, white, red, white,
       red, white, end))

# 不打印匹配的警告
warnings.filterwarnings('ignore')

# 创建解析步骤
parser = argparse.ArgumentParser()
# 添加参数步骤
parser.add_argument('-u', '--url', help='root url', dest='root')  # dest:参数别名
parser.add_argument('-c', '--cookie', help='cookie', dest='cook')
parser.add_argument('-r', '--regex', help='regex pattern', dest='regex')
parser.add_argument('-e', '--export', help='export format', dest='export')
parser.add_argument('-o', '--output', help='output directory', dest='output')
parser.add_argument('-l', '--level', help='levels to crawl', dest='level',
                    type=int) # type:参数类型
parser.add_argument('-t', '--threads', help='number of threads', dest='threads',
                    type=int)
parser.add_argument('-d', '--delay', help='delay between requests',
                    dest='delay', type=float)
parser.add_argument('-s', '--seeds', help='additional seed URLs', dest='seeds',
                    nargs="+", default=[]) # nargs 应该读取的命令行参数个数，+ 表示一个或多个参数
parser.add_argument('--user-agent', help='custom user agent(s)',
                    dest='user_agent')
parser.add_argument('--exclude', help='exclude URLs matching this regex',
                    dest='exclude')
parser.add_argument('--timeout', help='http request timeout', dest='timeout',
                    type=float)

# 其它参数
parser.add_argument('--headers', help='add headers', dest='headers',
                    action='store_true')
parser.add_argument('--dns', help='enumerate subdomains and DNS data',
                    dest='dns', action='store_true')
parser.add_argument('--ninja', help='ninja mode', dest='ninja',
                    action='store_true')
parser.add_argument('--keys', help='find secret keys', dest='api',
                    action='store_true')
parser.add_argument('--only-urls', help='only extract URLs', dest='only_urls',
                    action='store_true')
args = parser.parse_args() # 返回一个命名空间，如果想要使用变量，可用 args.attr

headers = args.headers  # 提供headers
delay = args.delay or 0  # 请求延时，默认为 0
timeout = args.timeout or 6  # HTTP请求超时，默认为 6
cook = args.cook or None  # Cookie，默认为 None
api = bool(args.api)  # 判断是否有API，是布尔类型
ninja = bool(args.ninja)  # 切换Ninja模式
crawl_level = args.level or 2  # 爬取的层数，默认为2层
thread_count = args.threads or 2  # 线程数，默认为2个线程
only_urls = bool(args.only_urls)  # only_urls默认为False


# 预先定义一些变量我们将在后面的代码中用来存储值，set() 是无序不重复元素集
keys = set()  # 密钥
files = set()  # pdf、css、png 等类型的文件
intel = set()  # 邮箱地址、网站账号等网络相关信息
robots = set()  # robots.txt文件
custom = set()  # 由自定义的正则表达式匹配的字符串
failed = set()  # 没有成功爬取的URLs
scripts = set()  # JS文件
external = set()  # 不属于目标网站范围的URLs
fuzzable = set()  # 已在其中获取参数的网址，比如：example.com/page.php?id=2
endpoints = set()  # 从JS文件中找到的URLs
processed = set()  # 已爬取过的URLs
internal = set([s for s in args.seeds])  # 属于目标网站范围内的URLs

bad_intel = set()  # 失效的网站URLs
bad_scripts = set()  # 失效的JS文件URLs


# 处理 http 请求头
if headers:
    headers = extract_headers(prompt())  # 这里涉及到 core/utils.py 文件中的 extract_headers() 函数、core/prompt.py 文件中的 prompt() 函数


# 如果用户已经提供了一个URL
if args.root:
    main_inp = args.root
    if main_inp.endswith('/'): # 如果该URL以 '/' 结尾
        # 使用切片的方式移除它，因为它可能会在后续的代码中造成问题
        main_inp = main_inp[:-1]
# 如果用户没有提供一个URL
else:
    print('\n' + parser.format_help().lower()) # 打印命令行参数用法提示信息并退出
    quit()

# 如果用户提供的 root url 没有 http 或者 http(s)，需要处理一下数据
if main_inp.startswith('http'): # 如果是以 http 开头则直接使用该 URL
    main_url = main_inp
else:
    try:
        requests.get('https://' + main_inp) # 否则尝试给URL添加 https:// 并验证是否可以请求
        main_url = 'https://' + main_inp
    except:
        main_url = 'http://' + main_inp # 请求不成功就添加 http://

schema = main_url.split('//')[0] # 看是 https: 或 http:
# 添加 root url 到 internal 方便爬取
internal.add(main_url)

# 从 url 中提取 host
host = urlparse(main_url).netloc
# 定义输出路径为用户指定路径或者默认为 host
output_dir = args.output or host
# 提取顶级域名
try:
    domain = top_level(main_url) # 这里涉及到 core/utils.py 文件中的 top_level() 函数
except:
    domain = host


# 确定用户头文件，如果有提供就使用提供的，如果没有提供就使用 core/user-agents.txt 文件中的数据
if args.user_agent:
    user_agents = args.user_agent.split(',')
else:
    with open(sys.path[0] + '/core/user-agents.txt', 'r') as uas: # 这里涉及到 core/user-agents.txt 文件
        user_agents = [agent.strip('\n') for agent in uas]


supress_regex = False

def intel_extractor(response):
    """从返回的响应体中提取intel"""
    matches = re.findall(r'([\w\.-]+s[\w\.-]+\.amazonaws\.com)|([\w\.-]+@[\w\.-]+\.[\.\w]+)', response)
    if matches:
        for match in matches:
            bad_intel.add(match)

def js_extractor(response):
    """从返回的响应体中提取JS文件"""
    matches = re.findall(r'<(script|SCRIPT).*(src|SRC)=([^\s>]+)', response)
    for match in matches:
        match = match[2].replace('\'', '').replace('"', '')
        bad_scripts.add(match)

def extractor(url):
    """从响应体中提取具体的信息"""
    response = requester(url, main_url, delay, cook, headers, timeout, host, ninja, user_agents, failed, processed) # 这里涉及到 core/requester.py 文件中的 requester() 函数

    matches = re.findall(r'<[aA].*(href|HREF)=([^\s>]+)', response)
    for link in matches:
        # 移除"#"后的所有内容以处理页内锚点
        link = link[1].replace('\'', '').replace('"', '').split('#')[0]
        # 检查这些 URLs 是否应该被爬取
        if is_link(link, processed, files): # 这里涉及到 core/utils.py 文件中的 is_link() 函数
            if link[:4] == 'http':
                if link.startswith(main_url):
                    internal.add(link)
                else:
                    external.add(link)
            elif link[:2] == '//':
                if link.split('/')[2].startswith(host):
                    internal.add(schema + link)
                else:
                    external.add(link)
            elif link[:1] == '/':
                internal.add(main_url + link)
            else:
                internal.add(main_url + '/' + link)

    if not only_urls:
        intel_extractor(response)
        js_extractor(response)
    if args.regex and not supress_regex:
        regxy(args.regex, response, supress_regex, custom) # 这里涉及到 core/utils.py 文件中的 regxy() 函数
    if api:
        matches = re.findall(r'[\w-]{16,45}', response)
        for match in matches:
            if entropy(match) >= 4: # 这里涉及到 core/utils.py 文件中的 entropy() 函数
                keys.add(url + ': ' + match)


def jscanner(url):
    """从JS代码中提取端点"""
    response = requester(url, main_url, delay, cook, headers, timeout, host, ninja, user_agents, failed, processed)  # 这里涉及到 core/requester.py 文件中的 requester() 函数
    # 提取 URLs/endpoints
    matches = re.findall(r'[\'"](/.*?)[\'"]|[\'"](http.*?)[\'"]', response)
    # 遍历 matches, match 是一个元组
    for match in matches:
        # 进行组合，因为其中一项总是空的
        match = match[0] + match[1]
        # 确保其中没有一些JS代码
        if not re.search(r'[}{><"\']', match) and not match == '/':
            endpoints.add(match)


# 在爬取开始的时候记录一个时间值
then = time.time()

# 第一步：从 robots.txt 和 sitemap.xml 文件中提取 urls 
zap(main_url, domain, host, internal, robots) # 这里涉及到 core/zap.py 文件中的 zap() 函数

# 这是第一层，emails 也可以被解析
internal = set(remove_regex(internal, args.exclude)) # 这里涉及到 core/utils.py 文件中的 remove_regex() 函数

# 第二步：递归爬取在 crawl_level 中指定的限制层数
for level in range(crawl_level):
    # 需要爬取的链接数 =（所有的链接数 - 已经爬取过的链接数）- 不需要爬取的链接数
    links = remove_regex(internal - processed, args.exclude)
    # 如果需要爬取的链接数是 0，即：所有的链接都爬取过了
    if not links:
        break
    # 如果爬取过的链接数大于所有的链接数
    elif len(internal) <= len(processed):
        if len(internal) > 2 + len(args.seeds):
            break
    print('%s Level %i: %i URLs' % (run, level + 1, len(links)))
    try:
        flash(extractor, links, thread_count) # 这里涉及到 core/flash.py 文件中的 flash() 函数
    except KeyboardInterrupt:
        print('')
        break

if not only_urls:
    for match in bad_scripts:
        if match.startswith(main_url):
            scripts.add(match)
        elif match.startswith('/') and not match.startswith('//'):
            scripts.add(main_url + match)
        elif not match.startswith('http') and not match.startswith('//'):
            scripts.add(main_url + '/' + match)
    # 第三步：遍历JS文件来获取端点
    print('%s Crawling %i JavaScript files' % (run, len(scripts)))
    flash(jscanner, scripts, thread_count)

    for url in internal:
        if '=' in url:
            fuzzable.add(url)

    for match in bad_intel:
        for x in match:  # 因为 match 是一个元组
            if x != '':  # 如果这个值不为空
                intel.add(x)
        for url in external:
            try:
                if top_level(url, fix_protocol=True) in intels:
                    intel.add(url)
            except:
                pass

# 记录下爬取停止的时间
now = time.time()
# 计算总耗费时间
diff = (now - then)
minutes, seconds, time_per_request = timer(diff, processed) # 这里涉及到 core/utils.py 文件中的 timer() 函数

# 第四步：保存这个结果
if not os.path.exists(output_dir): # 如果这个文件夹不存在
    os.mkdir(output_dir) # 创建新的文件夹

datasets = [files, intel, robots, custom, failed, internal, scripts,
            external, fuzzable, endpoints, keys]
dataset_names = ['files', 'intel', 'robots', 'custom', 'failed', 'internal',
                 'scripts', 'external', 'fuzzable', 'endpoints', 'keys']

writer(datasets, dataset_names, output_dir) # 这里涉及到 core/utils.py 文件中的 writer() 函数
# 打印我们的结果
print(('%s-%s' % (red, end)) * 50)
for dataset, dataset_name in zip(datasets, dataset_names):
    if dataset:
        print('%s %s: %s' % (good, dataset_name.capitalize(), len(dataset)))
print(('%s-%s' % (red, end)) * 50)

print('%s Total requests made: %i' % (info, len(processed)))
print('%s Total time taken: %i minutes %i seconds' % (info, minutes, seconds))
print('%s Requests per second: %i' % (info, int(len(processed)/diff)))



datasets = {
    'files': list(files), 'intel': list(intel), 'robots': list(robots),
    'custom': list(custom), 'failed': list(failed), 'internal': list(internal),
    'scripts': list(scripts), 'external': list(external),
    'fuzzable': list(fuzzable), 'endpoints': list(endpoints),
    'keys' : list(keys)
}

if args.dns:
    print('%s Enumerating subdomains' % run)
    from plugins.find_subdomains import find_subdomains # 这里涉及到 plugins/find_subdomains.py 文件中的 find_subdomains() 函数
    subdomains = find_subdomains(domain)
    print('%s %i subdomains found' % (info, len(subdomains)))
    writer([subdomains], ['subdomains'], output_dir)
    datasets['subdomains'] = subdomains
    from plugins.dnsdumpster import dnsdumpster # 这里涉及到 plugins/dnsdumpster.py 文件中的 dnsdumpster() 函数
    print('%s Generating DNS map' % run)
    dnsdumpster(domain, output_dir)

if args.export:
    from plugins.exporter import exporter
    exporter(output_dir, args.export, datasets) #  这里涉及到 plugins/exporter.py 文件中的 exporter() 函数

print('%s Results saved in %s%s%s directory' % (good, green, output_dir, end))
