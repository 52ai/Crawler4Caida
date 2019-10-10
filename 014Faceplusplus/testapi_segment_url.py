#coding:utf-8
"""
create on Oct 10,2019 by Wayne
Fun:test face++ Human Body Segment api

curl -X POST "https://api-cn.faceplusplus.com/humanbodypp/v2/segment" -F "api_key=MvZmIZt2ZzDjsbe8IJ7esRHr3dT5MGnH"  -F "api_secret=9S6vZXUmNv095AAIcR1m7oJ90-8qdJEJ"  -F "image_url=http://file.elecfans.com/web1/M00/4F/15/o4YBAFrRd8WATt6oAAQlH7olQ2s926.png"  -F "return_grayscale=0"
"""
import urllib.request
import urllib.error
import time
import json
import base64

http_url = 'https://api-cn.faceplusplus.com/humanbodypp/v2/segment'
key = "MvZmIZt2ZzDjsbe8IJ7esRHr3dT5MGnH"
secret = "9S6vZXUmNv095AAIcR1m7oJ90-8qdJEJ"
filepath = r"img/demo.png"

boundary = '----------%s' % hex(int(time.time() * 1000))
data = []
data.append('--%s' % boundary)
data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
data.append(key)
data.append('--%s' % boundary)
data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
data.append(secret)
data.append('--%s' % boundary)
fr = open(filepath, 'rb')
data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
data.append('Content-Type: %s\r\n' % 'application/octet-stream')
data.append(fr.read())
fr.close()

# print(data) #  本地图像数据已格式化为字符串

data.append('--%s' % boundary)
data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_grayscale')
data.append('0')
data.append('--%s\r\n' % boundary)

print(data)

for i, d in enumerate(data):
    if isinstance(d, str):
        data[i] = d.encode('utf-8')

http_body = b'\r\n'.join(data)

# 构建http 请求
req = urllib.request.Request(url=http_url, data=http_body)

# 为构建的http 请求添加头部
req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)

try:
    # 向服务器发起post请求
    post_resq = urllib.request.urlopen(req, timeout=5)
    # 得到response
    qrcont = post_resq.read()
    print(qrcont.decode('utf-8'))
    hjson = json.loads(qrcont)
    with open("./img/testapi_usingRequests_seg.jpg", "wb") as file:
        decode_base = base64.b64decode(hjson['body_image'])
        file.write(decode_base)
except urllib.error.HTTPError as e:
    print(e.read().decode('utf-8'))




