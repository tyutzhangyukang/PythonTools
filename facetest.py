import requests
import sys
import urllib
import json
import base64


#url = 'http://10.240.26.34:8008/audio'
#url ='http://10.240.126.8:8008/audio'
#url = 'http://172.23.69.49:80/audio'
url = 'http://localhost:8008/audio'
bytesStr = base64.b64encode(open(sys.argv[1]).read())

d = {"wav_str": bytesStr,'output_mode_str':sys.argv[2], 'jie_ba_str':'jie_ba_once_no'}

e = urllib.urlencode(d)

n = requests.post(url, data=e, headers={"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"})
yy = json.loads(n.text)
print(yy)
