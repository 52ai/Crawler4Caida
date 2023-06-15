# coding: utf-8
"""
create on Jun 14, 2023 By Wayne YU
Email: ieeflsyu@outlook.com

Function:

测试scapy相关功能，感觉这个库是从数据面探测网络空间的重要突破口

"""
from scapy.all import sr, IP, ICMP, Ether, TCP, sr1, UDP, DNS, srp, wrpcap, rdpcap, sniff, lsc, arping, traceroute
import time


ans, un_ans = sr(IP(dst='111.8.18.2')/ICMP())
ans.summary(lambda s, r: r.sprintf("%IP.src% is alive"))
un_ans.show()

p = Ether() / IP(dst="www.mryu.top") / TCP(flags="F")
print(p.summary())

print(p.dst)
print(p[IP].src)
print(p.sprintf("%Ether.src% > %Ether.dst%\n%IP.src% > %IP.dst%"))

print([p for p in IP(ttl=(1, 5)) / ICMP()])

print([p for p in IP() / TCP(dport=[22, 80, 443])])  # specific values

# the sr1() function sends a packet a returns a reply
# Scapy can match queries and answers
print("-------test sr1()---------")
p = sr1(IP(dst="218.201.1.249") / UDP() / DNS())
print(p[DNS].an)


# the srp() function sends a list of frames and returns two variables
# r a list of queries and matched answers
# u a list of unanswered packets
print("-------test srp()---------")
# r, u = srp(Ether() / IP(dst="8.8.8.8", ttl=(5, 10)) / UDP() / DNS())
# print(r)
# print(u)
#
# # Access the first tuple
# print(r[0][0].summary())  # sent packet
# print(r[0][1].summary())  # received packet
#
# # Scapy received an ICMP time-exceeded
# print(r[0][1][ICMP])

wrpcap("scapy.pcap", ans)
pcap_p = rdpcap("scapy.pcap")

for item_p in pcap_p:
    print(item_p)

s = sniff(count=2)
print(s)
sniff(count=2, prn=lambda p: p.summary)

# the lsc() function lists available commands
print(lsc())

print(arping("192.168.197.0/24"))
print(help(traceroute))


def qos_ping(host, count=10):
    qos_p = Ether()/IP(dst=host)/ICMP()
    t = 0.0
    for x in range(count):
        t1 = time.time()
        qos_ans = srp(qos_p, iface="WLAN", verbose=0)
        print(qos_ans)
        t2 = time.time()
        t += t2 - t1
    return (t / count) * 1000


print(qos_ping('218.201.1.249'), "ms")


def traceroute(destination, max_hops):
    ttl = 1
    while ttl <= max_hops:
        # Create the ICMP Echo Request packet with the specified TTL
        tr_p = IP(dst=destination, ttl=ttl) / ICMP()

        # Send the packet and record the start time
        start_time = time.time()
        reply = sr1(tr_p, verbose=False, timeout=1)

        if reply is None:
            # No reply received, print a timeout message
            print(f"{ttl}. * * *")
        elif reply.type == 0:
            # Echo Reply received, we've reached the destination
            print(f"{ttl}. {reply.src}  {round((time.time() - start_time) * 1000, 2)} ms")
            break
        else:
            # We've received a Time Exceeded message, continue to the next hop
            print(f"{ttl}. {reply.src}  {round((time.time() - start_time) * 1000, 2)} ms")

        ttl += 1

    # Usage example


traceroute("218.201.1.249", 30)
