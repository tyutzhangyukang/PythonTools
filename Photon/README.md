实验楼学习记录：
1. 依赖环境
sudo pip3 install --upgrade pip
sudo pip3 install -r requests urllib3 tld

主要特征
数据提取

Photon 在爬取的过程中可以提取以下的数据：

URLs
带参数的 URLs（example.com/gallery.php?id=2）
Intel（邮箱，社交媒体账户，亚马逊存储桶等）
文件（pdf、png、xml 等）
密钥（auth/API keys & hashes）
JS 文件 & 其中的端点
能够匹配自定义正则表达式的字符串
子域名 & DNS 有关的数据
这些信息可以按照有序的方式进行保存或者导出为 json 格式。

可自由定义

控制超时、延时，包括 URLs 正则匹配模式和其它东西，有大量的操作可以提供。

特点

Photon 提供小的线程管理从而能够提升爬取的效率。

可以通过 --ninja 选项开启 Ninja 模式，4 台在线的服务可以提供使用去发送请求。

2. usage: photon.py [options]

  -u --url              root url    # 根url
  -l --level            levels to crawl    # 爬取的条数
  -t --threads          number of threads    # 线程数量
  -d --delay            delay between requests    # 请求延迟
  -c --cookie           cookie    # 存储在用户本地终端上的数据
  -r --regex            regex pattern    # 正则表达式
  -s --seeds            additional seed urls    # 额外的种子urls
  -e --export           export formatted result   # 导出不同样式的结果
  -o --output           specify output directory    # 指明导出的目录
  --keys                extract secret keys    # 提取密钥
  --exclude             exclude urls by regex    # 使用正则表达式排查urls
  --timeout             http requests timeout    # http 请求超时
  --ninja               ninja mode    # ninja 模式
  --headers             supply http headers    # 支持 http 请求头
  --dns                 enumerate subdomains & dns data    # 列举子域名和dns数据
  --only-urls           only extract urls    # 只导出urls
  --user-agent          specify user-agent(s)    # 指定 用户代理
  
3. 