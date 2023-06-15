# coding: utf-8
"""
create on Jun 14, 2023 By Wayne YU
Email: ieeflsyu@outlook.com

Function:

测试scapy相关功能，感觉这个库是从数据面探测网络空间的重要突破口

"""
import sys
from scapy.all import sr, sr1, IP, ICMP

ans, unans = sr(IP(dst='111.8.18.2')/ICMP())
ans.summary(lambda s, r: r.sprintf("%IP.src% is alive"))
unans.show()



