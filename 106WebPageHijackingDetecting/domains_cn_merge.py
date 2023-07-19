# coding: utf-8
"""
create on Jul. 17, 2023 By Wayne YU
Email: ieeflsyu@outlook.com


Function:

将.cn、dns+ip location(sun)、DaTang11w三个库的cn domains合并

"""

dot_cn_file = "../000LocalData/106WebPage/cn_domains_37200.csv"
dns_ip_domains_file = "../000LocalData/106WebPage/domain-9w-sun-cn.csv"
DaTang11w_file = "../000LocalData/106WebPage/domain-11w-caict-cn.txt"
host10m_dot_cn_file = "../000LocalData/106WebPage/host10m.csv"

domains_cn_merge = []


with open(dot_cn_file, "r", encoding="utf-8") as f:
    for domain in f.readlines():
        domain = domain.strip()
        # print(domain)
        domains_cn_merge.append(domain)

with open(dns_ip_domains_file, "r", encoding="utf-8") as f:
    for domain in f.readlines():
        domain = domain.strip()
        # print(domain)
        domains_cn_merge.append(domain)

with open(DaTang11w_file, "r", encoding="utf-8") as f:
    for domain in f.readlines():
        domain = domain.strip().strip("www.")
        # print(domain)
        domains_cn_merge.append(domain)


print("domains cn all:", len(domains_cn_merge))
print("domains cn merge:", len(set(domains_cn_merge)))

with open("../000LocalData/106WebPage/domains_cn_merge.csv", "w", encoding="utf-8") as f:
    for item in set(domains_cn_merge):
        f.writelines(item+"\n")
    print("write domains_cn_merge.csv success!")
