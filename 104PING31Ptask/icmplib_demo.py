# coding: utf-8
"""

create on Jun 14, 2023 By Wayne YU
Email: ieeflsyu@outlook.com

Function:

测试icmplib的相关功能

"""

from icmplib import ping, traceroute


host = ping('112.29.0.190', count=3, interval=0.2)
print("host IP:", host.address)
print("Min RTT:", host.min_rtt, "ms")
print("AVG RTT:", host.avg_rtt, "ms")
print("MAX RTT:", host.max_rtt, "ms")
print(host.rtts)
print("Packets Sent:", host.packets_sent)
print("Packets Received:", host.packets_received)
print("Packets Loss:", host.packet_loss)
print("Jitter:", host.jitter)
print("Is Alive:", host.is_alive)


hops = traceroute('bing.com', count=1, interval=0.01, timeout=1, first_hop=1, max_hops=30, fast=True)
print('Distance/TTL    Address    Average round-trip time')
last_distance = 0

for hop in hops:
    if last_distance + 1 != hop.distance:
        print('Some gateways are not responding')

    # See the Hop class for details
    print(f'{hop.distance}    {hop.address}    {hop.avg_rtt} ms')
    last_distance = hop.distance
