# coding: utf-8
"""
create on Feb 15, 2023 By Wayne YU
Email: ieeflsyu@outlook.com

Function:

测试shadowsocks proxy

经测试使用ChatGPT生成的shadowsocks样例代码，存在很多的错误，如参数错位等，无法运行
测试到此为止，后续若想通过Python使用shadowsocks代理，再做研究吧

"""

import requests
from shadowsocks import encrypt

# 配置Shadowsocks代理服务器地址和端口
shadowsocks_proxy = {
    'socks5': 'socks5://nusad7y.cdn.dogenode.xyz:8871',
    'http': 'http://nusad7y.cdn.dogenode.xyz:8871',
    'https': 'https://nusad7y.cdn.dogenode.xyz:8871'
}

# 配置Shadowsocks代理服务器的密码和加密方式
shadowsocks_password = '0C1ZFh'
shadowsocks_method = 'chacha20-ietf-poly1305'

# 配置requests使用Shadowsocks代理
session = requests.session()
session.proxies.update(shadowsocks_proxy)
session.headers.update({'User-Agent': 'Mozilla/5.0'})
session.verify = False

# 配置Shadowsocks加密方式
encryptor = encrypt.Encryptor(shadowsocks_password, shadowsocks_method)

# 使用Shadowsocks代理访问网站
response = session.get('https://www.google.com/search?q=%E4%BA%91%E4%B8%AD%E5%B8%83%E8%A1%A3', stream=True)
for chunk in response.iter_content(chunk_size=1024):
    if chunk:
        decrypted_chunk = encryptor.decrypt(chunk)
        # 处理解密后的数据
        print(decrypted_chunk)
