#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import gevent
from gevent import monkey

import dns
import dns.resolver
import os
import json
import time
import socket
from decimal import Decimal

LOCAL_MONITOR_HOSTNAME = os.environ.get('LOCAL_M_HOSTNAME')
if LOCAL_MONITOR_HOSTNAME is None or len(LOCAL_MONITOR_HOSTNAME) == 0:
    LOCAL_MONITOR_HOSTNAME = socket.gethostname()
    os.environ['LOCAL_M_HOSTNAME'] = LOCAL_MONITOR_HOSTNAME

#print(LOCAL_MONITOR_HOSTNAME)

FALCON_PUSH_STEP = 10

dnsserver = "168.63.129.16"
ts = int(time.time())

external_test_records = [
    {"query": "kuaishoupay.com", "qtype": "A"},
    {"query": "kuaishou.com", "qtype": "A"},
    {"query": "baidu.com", "qtype": "A"},
    {"query": "qq.com", "qtype": "A"},
    {"query": "google.com", "qtype": "A"},
    {"query": "facebook.com", "qtype": "A"},
]

internal_test_records = [
    {"query": "bjpg-rs4542.yz02", "qtype": "A"},
    {"query": "kml.corp.kuaishou.com", "qtype": "A"},
    {"query": "git.corp.kuaishou.com", "qtype": "A"},
    {"query": "perf-gateway.internal", "qtype": "A"},
    {"query": "ipip.internal", "qtype": "A"},
]

def print_data(msg):
    print_text=time.ctime()+' '+json.dumps(msg)+'\n'
    f = open("ks-168.63.129.16.log",'a')
    f.write(print_text)
    f.close()
    #print(time.ctime(),json.dumps(msg))

def test_records(dnsserver,resolver,records):
    jobs = []
    total_cnt = 0
    success_cnt = 0
    for record in records:
        query_result = dns_query(dnsserver,resolver,record["query"],record["qtype"])
        print_text=time.ctime()+' ' +record["query"] +' '+str(query_result)+'\n'
        f = open("ks-168.63.129.16.log",'a')
        f.write(print_text)
        f.close()
        #print(time.ctime(),record["query"],query_result)
        if query_result:
            success_cnt += 1
        total_cnt += 1
    #print(total_cnt,success_cnt)
    return total_cnt, success_cnt

def dns_query(dnsserver,resolver,query,qtype):
    try:
        resolver.nameservers=[dnsserver]
        resolver.lifetime = 2
        result = resolver.query(query, rdtype=qtype, tcp=False)
    except Exception as e:
        print_text=time.ctime()+' dns'+dnsserver+' failed test record: type '+ qtype +' query '+e.__class__.__name__+' '+ str(e)+'\n'
        f = open("ks-168.63.129.16.log",'a')
        f.write(print_text)
        f.close()
        #print(time.ctime(),"dns %s failed test record: type %s, query %s, %s: %s" % (dnsserver, qtype, query, e.__class__.__name__, str(e)))
        return False
    return True

def dns_sla():
    resolver = dns.resolver.Resolver()
    #resolver.lifetime = 1

    external_total=external_success=0
    #internal_total=internal_success=0

    #int_total, int_success = test_records(dnsserver, resolver, internal_test_records)
    #internal_total += int_total
    #internal_success += int_success
    ext_total, ext_success = test_records(dnsserver, resolver, external_test_records)
    external_total += ext_total
    external_success += ext_success
    #int_sla = Decimal(int_success) / Decimal(int_total)
    ext_sla = Decimal(ext_success) / Decimal(ext_total)

    payload = [
#        {
#            "endpoint": LOCAL_MONITOR_HOSTNAME,
#            "metric": "bind9.internal.sla",
#            "timestamp": ts,
#            "step": FALCON_PUSH_STEP,
#            "value": float(int_sla),
#            "counterType": "GAUGE",
#        },
        {
            "endpoint": LOCAL_MONITOR_HOSTNAME,
            "metric": "bind9.external.sla",
            "timestamp": ts,
            "step": FALCON_PUSH_STEP,
            "value": float(ext_sla),
            "counterType": "GAUGE",
        }
    ]
    print_text=str(payload)+'\n'
    f = open("ks-168.63.129.16.log",'a')
    f.write(print_text)
    f.close()
    #print_data(payload)

if __name__ == '__main__':
    while True:
        dns_sla()
        time.sleep(20)
