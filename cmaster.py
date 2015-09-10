#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Chengzhe Yan
# @Date:   2015-09-08 14:44:39
# @Last Modified by:   Chengzhe Yan
# @Last Modified time: 2015-09-10 21:48:08


# This light weighted cluster management is written from small high-
# performance computing cluster. Cmaster.py works as master of cluster
# management, accepting stat data from goat nodes, save the stats in the
# server pool, and response queries from clients. The communication is by
# sending and receiving json containing the meta information.

import json
import time
import sys
import SocketServer
from daemon import runner

class server_info:
	last_update = -1
	server_meta = None
	def __init__(self):
		self.last_update = -1
		self.server_meta = None

servers = dict()

class master_on_receive(SocketServer.BaseRequestHandler):
	def handle(self):
		data = self.request[0].strip()
		socket = self.request[1]
		msg = json.loads(data)
# print msg
		if msg['prtc'] == 1:
			# request for cluster stats
			pack = dict()
			for key, value in servers.iteritems():
				pack[key] = value.server_meta
				pack[key]['lu'] = value.last_update
			rmsg = json.dumps(pack)
			socket.sendto(rmsg, self.client_address)
		elif msg['prtc'] == 2:
			# server meta
			# check for existing meta pieces
			if servers.get(msg['name']) == None:
				servers[msg['name']] = server_info()
			servers[msg['name']].server_meta = msg
			servers[msg['name']].last_update = time.time()

class MasterApp():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/var/log/collie.log'
        self.stderr_path = '/var/log/collie.err'
        self.pidfile_path =  '/var/run/collie.pid'
        self.pidfile_timeout = 5
            
    def run(self):
		config = json.loads(open(sys.argv[2]).read())
		server = SocketServer.UDPServer((config['ip'], config['port']), master_on_receive)
		server.serve_forever()


if __name__ == "__main__":
	A = MasterApp()
	daemon_runner = runner.DaemonRunner(A)
	daemon_runner.do_action()
