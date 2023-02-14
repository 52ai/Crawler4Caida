# coding: utf-8
"""
create on Feb 14, 2023 By Wayne YU
Email: ieeflsyu@outlook.com

Function:

测试ChatGPT的API接口

"""

import requests
import json


key_file = ".key/openai_key.txt"
with open(key_file, 'r', encoding='utf-8') as f:
    line = f.readlines()[0].strip()
    print(line)
    key_string = line

url = "http://api.openai.com/v1/engines/davinci-codex/completions"

data = {
    "prompt": "Hello, how are you?",
    "temperature": 0.7,
    "max_tokens": 60,
    "top_p": 1,
    "n": 1,
    "stop": "\n"
}

# 设置Shadowsocks代理服务器的地址和端口号
proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer <{key_string}>"
}

# response = requests.post(url, headers=headers, data=json.dumps(data), proxies=proxies)
response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    response_data = json.loads(response.content)
    completions = response_data["choices"][0]["text"]
    print(completions)
else:
    print(f"Error: {response.status_code}")

