#coding:utf-8
"""
create on Oct 10,2019 by Wayne
Fun:test face++ Human Body Segment api

curl -X POST "https://api-cn.faceplusplus.com/humanbodypp/v2/segment" -F "api_key=MvZmIZt2ZzDjsbe8IJ7esRHr3dT5MGnH"  -F "api_secret=9S6vZXUmNv095AAIcR1m7oJ90-8qdJEJ"  -F "image_url=http://file.elecfans.com/web1/M00/4F/15/o4YBAFrRd8WATt6oAAQlH7olQ2s926.png"  -F "return_grayscale=0"
"""
import subprocess
import json
import base64

# file_path = r'img/demo.png'
# boundary = '----------%s' % hex(int(time.time() * 1000))
# data = []
# data.append('--%s' % boundary)
# data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
# data.append(key)
# data.append('--%s' % boundary)
# data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
# data.append(secret)
# data.append('--%s' % boundary)
# fr = open(filepath, 'rb')
# data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
# data.append('Content-Type: %s\r\n' % 'application/octet-stream')
# data.append(fr.read())
# fr.close()

cmd_str = 'curl -X POST "https://api-cn.faceplusplus.com/humanbodypp/v2/segment" -F "api_key=MvZmIZt2ZzDjsbe8IJ7esRHr3dT5MGnH"  -F "api_secret=9S6vZXUmNv095AAIcR1m7oJ90-8qdJEJ"  -F "image_url=http://file.elecfans.com/web1/M00/4F/15/o4YBAFrRd8WATt6oAAQlH7olQ2s926.png"  -F "return_grayscale=0" '
ftp_sub = subprocess.Popen(cmd_str, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
ret = ftp_sub.stdout.read()
str_ret = ret.decode('gbk')
print(str_ret)
hjson = json.loads(str_ret)
print(hjson['body_image'])
body_image_code = hjson['body_image']
# 将base64编码解码为图像

# file_image = open("./test_segment_result.jpg", "wb")
# decode_base =  base64.b64decode(body_image_code)
# file_image.write(decode_base)
# file_image.close()

with open("./img/test_segement_result.jpg", "wb") as file:
    decode_base = base64.b64decode(hjson['body_image'])
    file.write(decode_base)



