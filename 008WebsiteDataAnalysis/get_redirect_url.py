# coding:utf-8
"""
create on May 23,2019 by Wayne Yu
Function: find redirect url
"""
import requests

url =  """https://mclick.simba.taobao.com/cc_im?p=INC.redible&s=936271675&k=705&e=cf5Imw38zyT5LeEXLaoxX6gUJlv1pJiLeYS7ah10x8Plp95OWMW%2BVsso8ajx2qSZMHlKHH3GzaQJHiACcFM5PxMDWFwAo9PcY8S1Kuu7YOyaGIYBEZ9QdoMkKz82auCyNZ8bbUQVevFDzlFKxKHX%2Bp%2B%2FHAxpbvW62yiplFhHxAH%2BawzgNyHhNToiFWC%2FBivB3jGPPFqsRTmgWZf7Jshf%2F3NiXmDmL2WTZIU5wKgaeMLtxOLeyKFscBa2Gk%2FOQhS8QXtTBDucRxBcs%2BVbDLrgv3sZMGT3feX36D97LAShJd9MD5XRvHMkUiZ1X4oJf5e8A6wPbXazQ2BhHsqQJmOwW9ar422dxWmq6T1gXauzR9E6oGhtUAciYbZaIvTFPP5WiT5P4ZqSyXv%2FAAyqVXSIM8XLmjd2EBjqrva4CfegCkInOOBujZnCbYEbowsFHgfR4klATU%2BeMdP8aDAcIpvzCSUcQNNzEWczs6wXvWHBKPJKcRl8kP87KeIj1Nss8uZy6C8bX1UJGOX%2FKSRGD7W4PJ8izCG1Zvrbv1PWRmQ4wv%2B2uMM0StYEtjos6rPV5rBcSkwsiLYYrk1N%2BVEWn%2Fpm2D4q1HyKX658ob7TuonqLw7YJdkISO06Ojpj%2BnSXK0fDqKFI84lIBbCoaWX72cFm8FZSwYoxbzwwrE%2FS4mjROCmofgQh%2BXArHCoRdQ2u3FB%2B"""
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
response = requests.get(url, headers=headers)
# print(response.headers)
print(response.headers)
print(response.headers['Url-Hash'])

