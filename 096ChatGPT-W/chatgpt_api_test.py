# coding: utf-8
"""
create on Feb 14, 2023 By Wayne YU
Email: ieeflsyu@outlook.com

Function:

测试ChatGPT的API接口

"""

import requests
import json


# 设置Shadowsocks代理服务器的地址和端口号
proxies = {
    'http': 'socks5://127.0.0.1:7890',
    'https': 'socks5://127.0.0.1:7890'
}

key_file = ".key/openai_key.txt"
with open(key_file, 'r', encoding='utf-8') as f:
    line = f.readlines()[0].strip()
    print(line)
    api_key = line

# 现在，我们可以使用requests库来发出HTTP请求
# response = requests.get("http://httpbin.org/ip", proxies=proxies)
response = requests.get("http://httpbin.org/ip")

# print(response.json())
ip_address = response.json()["origin"]
# print(ip_address)
# 请求IP地址定位数据
response = requests.get('https://ipinfo.io/'+ip_address+'/json')

# 解析JSON响应
data = json.loads(response.text)
print(data)
# 输出IP地址定位数据
print('IP Address:', data['ip'])
print('City:', data['city'])
print('Country:', data['country'])


print("开始测试ChatGPT API")
"""
代码生成引擎：davinci-codex
自然语言生成引擎：text-davinci-002
"""

api_url = 'https://api.openai.com/v1/engines/text-davinci-002/completions'

# 输入的文本
prompt = "Which ISP is global Tier ISP, Please give me a list and the reason."
print("问题：", prompt)

# 调用API接口并获取响应
response = requests.post(api_url, headers={'Content-Type': 'application/json',
                                           'Authorization': f'Bearer {api_key}'},
                         json={'prompt': prompt, 'max_tokens': 2000, 'temperature': 0.7, 'n': 5})

# 解析响应JSON
result = response.json()["choices"][0]["text"].strip()
# print(response.json())
# 输出响应结果
print("回答:", result)

for item in response.json()["choices"]:
    print(item)

