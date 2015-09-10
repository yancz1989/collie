#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Chengzhe Yan
# @Date:   2015-09-08 14:44:22
# @Last Modified by:   Chengzhe Yan
# @Last Modified time: 2015-09-10 16:20:19

# This program works for cat stats from different servers in the cluster which
# help the job scheduler better manage work load between nodes in the cluster.

import json
import socket
import time
import datetime
import sys

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind(('166.111.131.97', 31200))
# socks = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# msg = dict()
# msg['prtc'] = 1
# socks.sendto(msg, {'166.111.131.85', 3120})

if __name__ == "__main__":
    HOST, PORT = "166.111.131.63", 3120
    query = dict()
    query['prtc'] = 1
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(query), (HOST, PORT))
    receive = sock.recv(4096)

    # parse json data
    ss = json.loads(receive)

    # show server status
    print '|# server | cpu | mem avail/total/used | gmem | gpu | last ack time|'
    for key, value in ss.iteritems():
    	print '| {} | {}% | {}/{}/{}% | {}% | {}% | {} |'.format(value['name'], value['cpu'],
    	 value['mem']['avail'], value['mem']['total'],value['mem']['usage'],
    	 # value['disk']['used'],value['disk']['total'],value['disk']['used'],
    	 value['gmem'], value['gpu'], datetime.datetime.fromtimestamp(value['lu']).strftime('%Y-%m-%d %H:%M:%S'))

print 'The following content can be pasted to you hosts file for easy connection. Enjoy your computing journey!\n'

for key, value in ss.iteritems():
	print '{}\t{}'.format(value['ipv4'], value['name'])

