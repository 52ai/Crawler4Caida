# coding:utf-8
"""
create on Sep 23, 2020 By Wenyan YU

Function:

前期已完成RIPE和RouteViews 50+个VP节点的实时路由数据采集
本程序将在前期工作的基础上，依托mrt2bgpdump程序，开展全球互联网BGP路由安全态势感知系统原型开发。

先从简单的开始，以5分钟进行切片，统计每个节点的U（N）（总的通告量）、U（A）（新增通告量）、U（W）（撤销通告量）的报文数量。
然后，综合各个VP节点的特征值，计算当前全球互联网网络路由威胁指数，实时监测是否存在重大网络安全事件正在发生或小型事故正在逐步扩大其影响范围。

"""
import sys
import argparse
import copy
from datetime import *
from mrtparse import *
import time
import os

peer = None


def parse_args(pre_args_str):
    # 创建一个解析对象
    p = argparse.ArgumentParser(
        description='This script converts to bgpdump format.')

    # 向解析对象p中添加我们关注的参数和选项
    p.add_argument(
        '-m', dest='verbose', default=False, action='store_true',
        help='one-line per entry with unix timestamps')

    p.add_argument(
        '-M', dest='verbose', action='store_false',
        help='one-line per entry with human readable timestamps(default format)')
    p.add_argument(
        '-O', dest='output', default=sys.stdout, nargs='?', metavar='file',
        type=argparse.FileType('w'),
        help='output to a specified file')
    p.add_argument(
        '-s', dest='output', action='store_const', const=sys.stdout,
        help='output to STDOUT(default output)')
    p.add_argument(
        '-v', dest='output', action='store_const', const=sys.stderr,
        help='output to STDERR')
    p.add_argument(
        '-t', dest='ts_format', default='dump', choices=['dump', 'change'],
        help='timestamps for RIB dumps reflect the time of the dump \
            or the last route modification(default: dump)')
    p.add_argument(
        '-p', dest='pkt_num', default=False, action='store_true',
        help='show packet index at second position')
    p.add_argument(
        'path_to_file',
        help='specify path to MRT format file')
    # 调用parse_args()进行解析
    return p.parse_args(pre_args_str)


class BgpDump:
    __slots__ = [
        'verbose', 'output', 'ts_format', 'pkt_num', 'type', 'num', 'ts',
        'org_time', 'flag', 'peer_ip', 'peer_as', 'nlri', 'withdrawn',
        'as_path', 'origin', 'next_hop', 'local_pref', 'med', 'comm',
        'atomic_aggr', 'aggr', 'as4_path', 'as4_aggr', 'old_state', 'new_state',
    ]

    def __init__(self, args):
        self.verbose = args.verbose
        self.output = args.output
        self.ts_format = args.ts_format
        self.pkt_num = args.pkt_num
        self.type = ''
        self.num = 0
        self.ts = 0
        self.org_time = 0
        self.flag = ''
        self.peer_ip = ''
        self.peer_as = 0
        self.nlri = []
        self.withdrawn = []
        self.as_path = []
        self.origin = ''
        self.next_hop = []
        self.local_pref = 0
        self.med = 0
        self.comm = ''
        self.atomic_aggr = 'NAG'
        self.aggr = ''
        self.as4_path = []
        self.as4_aggr = ''
        self.old_state = 0
        self.new_state = 0

    def print_line(self, prefix, next_hop):
        if self.ts_format == 'dump':
            d = self.ts
        else:
            d = self.org_time

        if self.verbose:
            d = str(d)
        else:
            d = datetime.utcfromtimestamp(d).\
                strftime('%m/%d/%y %H:%M:%S')

        if self.pkt_num:
            d = '%d|%s' % (self.num, d)

        if self.flag == 'B' or self.flag == 'A':
            self.output.write('%s|%s|%s|%s|%s|%s|%s|%s' % (
                self.type, d, self.flag, self.peer_ip, self.peer_as, prefix,
                self.merge_as_path(), self.origin))
            if self.verbose:
                self.output.write('|%s|%d|%d|%s|%s|%s|\n' % (
                    next_hop, self.local_pref, self.med, self.comm,
                    self.atomic_aggr, self.merge_aggr()))
            else:
                self.output.write('\n')
        elif self.flag == 'W':
            self.output.write('%s|%s|%s|%s|%s|%s\n' % (
                self.type, d, self.flag, self.peer_ip, self.peer_as,
                prefix))
        elif self.flag == 'STATE':
            self.output.write('%s|%s|%s|%s|%s|%d|%d\n' % (
                self.type, d, self.flag, self.peer_ip, self.peer_as,
                self.old_state, self.new_state))

    def print_routes(self):
        for withdrawn in self.withdrawn:
            if self.type == 'BGP4MP':
                self.flag = 'W'
            self.print_line(withdrawn, '')
        for nlri in self.nlri:
            if self.type == 'BGP4MP':
                self.flag = 'A'
            for next_hop in self.next_hop:
                self.print_line(nlri, next_hop)

    def td(self, m, count):
        self.type = 'TABLE_DUMP'
        self.flag = 'B'
        self.ts = m.ts
        self.num = count
        self.org_time = m.td.org_time
        self.peer_ip = m.td.peer_ip
        self.peer_as = m.td.peer_as
        self.nlri.append('%s/%d' % (m.td.prefix, m.td.plen))
        for attr in m.td.attr:
            self.bgp_attr(attr)
        self.print_routes()

    def td_v2(self, m):
        global peer
        self.type = 'TABLE_DUMP2'
        self.flag = 'B'
        self.ts = m.ts
        if m.subtype == TD_V2_ST['PEER_INDEX_TABLE']:
            peer = copy.copy(m.peer.entry)
        elif (m.subtype == TD_V2_ST['RIB_IPV4_UNICAST']
            or m.subtype == TD_V2_ST['RIB_IPV4_MULTICAST']
            or m.subtype == TD_V2_ST['RIB_IPV6_UNICAST']
            or m.subtype == TD_V2_ST['RIB_IPV6_MULTICAST']):
            self.num = m.rib.seq
            self.nlri.append('%s/%d' % (m.rib.prefix, m.rib.plen))
            for entry in m.rib.entry:
                self.org_time = entry.org_time
                self.peer_ip = peer[entry.peer_index].ip
                self.peer_as = peer[entry.peer_index].asn
                self.as_path = []
                self.origin = ''
                self.next_hop = []
                self.local_pref = 0
                self.med = 0
                self.comm = ''
                self.atomic_aggr = 'NAG'
                self.aggr = ''
                self.as4_path = []
                self.as4_aggr = ''
                for attr in entry.attr:
                    self.bgp_attr(attr)
                self.print_routes()

    def bgp4mp(self, m, count):
        self.type = 'BGP4MP'
        self.ts = m.ts
        self.num = count
        self.org_time = m.ts
        self.peer_ip = m.bgp.peer_ip
        self.peer_as = m.bgp.peer_as
        if (m.subtype == BGP4MP_ST['BGP4MP_STATE_CHANGE']
            or m.subtype == BGP4MP_ST['BGP4MP_STATE_CHANGE_AS4']):
            self.flag = 'STATE'
            self.old_state = m.bgp.old_state
            self.new_state = m.bgp.new_state
            self.print_line([], '')
        elif (m.subtype == BGP4MP_ST['BGP4MP_MESSAGE']
            or m.subtype == BGP4MP_ST['BGP4MP_MESSAGE_AS4']
            or m.subtype == BGP4MP_ST['BGP4MP_MESSAGE_LOCAL']
            or m.subtype == BGP4MP_ST['BGP4MP_MESSAGE_AS4_LOCAL']):
            if m.bgp.msg.type != BGP_MSG_T['UPDATE']:
                return
            for attr in m.bgp.msg.attr:
                self.bgp_attr(attr)
            for withdrawn in m.bgp.msg.withdrawn:
                self.withdrawn.append(
                    '%s/%d' % (withdrawn.prefix, withdrawn.plen))
            for nlri in m.bgp.msg.nlri:
                self.nlri.append('%s/%d' % (nlri.prefix, nlri.plen))
            self.print_routes()

    def bgp_attr(self, attr):
        if attr.type == BGP_ATTR_T['ORIGIN']:
            self.origin = ORIGIN_T[attr.origin]
        elif attr.type == BGP_ATTR_T['NEXT_HOP']:
            self.next_hop.append(attr.next_hop)
        elif attr.type == BGP_ATTR_T['AS_PATH']:
            self.as_path = []
            for seg in attr.as_path:
                if seg['type'] == AS_PATH_SEG_T['AS_SET']:
                    self.as_path.append('{%s}' % ','.join(seg['val']))
                elif seg['type'] == AS_PATH_SEG_T['AS_CONFED_SEQUENCE']:
                    self.as_path.append('(' + seg['val'][0])
                    self.as_path += seg['val'][1:-1]
                    self.as_path.append(seg['val'][-1] + ')')
                elif seg['type'] == AS_PATH_SEG_T['AS_CONFED_SET']:
                    self.as_path.append('[%s]' % ','.join(seg['val']))
                else:
                    self.as_path += seg['val']
        elif attr.type == BGP_ATTR_T['MULTI_EXIT_DISC']:
            self.med = attr.med
        elif attr.type == BGP_ATTR_T['LOCAL_PREF']:
            self.local_pref = attr.local_pref
        elif attr.type == BGP_ATTR_T['ATOMIC_AGGREGATE']:
            self.atomic_aggr = 'AG'
        elif attr.type == BGP_ATTR_T['AGGREGATOR']:
            self.aggr = '%s %s' % (attr.aggr['asn'], attr.aggr['id'])
        elif attr.type == BGP_ATTR_T['COMMUNITY']:
            self.comm = ' '.join(attr.comm)
        elif attr.type == BGP_ATTR_T['MP_REACH_NLRI']:
            self.next_hop = attr.mp_reach['next_hop']
            if self.type != 'BGP4MP':
                return
            for nlri in attr.mp_reach['nlri']:
                self.nlri.append('%s/%d' % (nlri.prefix, nlri.plen))
        elif attr.type == BGP_ATTR_T['MP_UNREACH_NLRI']:
            if self.type != 'BGP4MP':
                return
            for withdrawn in attr.mp_unreach['withdrawn']:
                self.withdrawn.append(
                    '%s/%d' % (withdrawn.prefix, withdrawn.plen))
        elif attr.type == BGP_ATTR_T['AS4_PATH']:
            self.as4_path = []
            for seg in attr.as4_path:
                if seg['type'] == AS_PATH_SEG_T['AS_SET']:
                    self.as4_path.append('{%s}' % ','.join(seg['val']))
                elif seg['type'] == AS_PATH_SEG_T['AS_CONFED_SEQUENCE']:
                    self.as4_path.append('(' + seg['val'][0])
                    self.as4_path += seg['val'][1:-1]
                    self.as4_path.append(seg['val'][-1] + ')')
                elif seg['type'] == AS_PATH_SEG_T['AS_CONFED_SET']:
                    self.as4_path.append('[%s]' % ','.join(seg['val']))
                else:
                    self.as4_path += seg['val']
        elif attr.type == BGP_ATTR_T['AS4_AGGREGATOR']:
            self.as4_aggr = '%s %s' % (attr.as4_aggr['asn'], attr.as4_aggr['id'])

    def merge_as_path(self):
        if len(self.as4_path):
            n = len(self.as_path) - len(self.as4_path)
            return ' '.join(self.as_path[:n] + self.as4_path)
        else:
            return ' '.join(self.as_path)

    def merge_aggr(self):
        if len(self.as4_aggr):
            return self.as4_aggr
        else:
            return self.aggr


def compute_threat_index(mrt_updates):
    """
    计算威胁指数
    :param mrt_updates:
    :return:
    """
    output_file_path = '../000LocalData/BGPData//output.txt'
    args_str = [mrt_updates, '-M', '-O', output_file_path]
    args = parse_args(args_str)
    # print(args)
    d = Reader(args.path_to_file)
    count = 0
    for m in d:
        m = m.mrt
        if m.err:
            continue
        b = BgpDump(args)
        if m.type == MRT_T['TABLE_DUMP']:
            b.td(m, count)
        elif m.type == MRT_T['TABLE_DUMP_V2']:
            b.td_v2(m)
        elif m.type == MRT_T['BGP4MP']:
            b.bgp4mp(m, count)
        count += 1

    # 读取生成的文件
    updates_all = 0  # 统计当前时间片全部BGP通告量
    with open(output_file_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            # print(line.strip())
            updates_all += 1
    print("统计当前时间片全部BGP通告量:", updates_all)


def gain_vp_ripe(root_path):
    """
    根据vp ripe的根目录路径，获取当前节点文件夹（即节点）
    :param root_path:
    :return file_new:
    """
    file_lists = os.listdir(root_path)
    file_lists.sort(key=lambda fn: os.path.getmtime(root_path + "\\" + fn))
    file_new = os.path.join(root_path, file_lists[-1])
    print(file_new)
    return file_new


if __name__ == '__main__':
    time_start = time.time()
    vp_ripe_root = "../000LocalData/BGPData/ripe/live_data/rrc00"
    while True:
        try:
            vp_ripe_latest = gain_vp_ripe(vp_ripe_root)
            compute_threat_index(vp_ripe_latest)
        except Exception as e:
            print("Error:", e)
        time.sleep(5*60)  # 休眠5分钟
        time_end = time.time()
        print("Running Time:", (time_end - time_start), "S")
