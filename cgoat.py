#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Chengzhe Yan
# @Date:   2015-09-08 17:02:29
# @Last Modified by:   Chengzhe Yan
# @Last Modified time: 2015-09-10 22:02:00

# Goat client script running for continuously sending data to master server.
# Meta data include ip address and computer system load.

import json
import socket
import time
import netifaces as ni
import psutil as ps
import subprocess as sp
import re
import sys
from daemon import runner

def collect_info(config):
	info = dict()

	# obtain ipv4/ipv6 address
	info['ipv4'] = ni.ifaddresses(config['conn_if'])[ni.AF_INET][0]['addr']
	info['ipv6'] = ni.ifaddresses(config['conn_if'])[ni.AF_INET6][0]['addr']

	# obtain memory usage
	mem_info = ps.virtual_memory()
	info['mem'] = dict()
	info['mem']['total'] = round(mem_info[0] * 1.0 / pow(2, 30), 2)
	info['mem']['avail'] = round(mem_info[1] * 1.0 / pow(2, 30), 2)
	info['mem']['usage'] = mem_info[2]

	# obtain cpu usage
	info['cpu'] = ps.cpu_percent()

	# obtain gpu/gmem usage
	if config['with_gpu'] == "no":
		info['gpu'] = -1
		info['gmem'] = -1
	else:
		out = sp.check_output('nvidia-smi | grep %', shell = True)
		rgpu = re.compile('\d+%')
		pgpu = rgpu.findall(out)
		gpu = 0.0
		for x in range(1, len(pgpu), 2):
			gpu = gpu + float(pgpu[x].strip('%'))
		info['gpu'] = gpu / len(pgpu) * 2

		# obtain gpu memory information
		rgmem = re.compile('\d+MiB')
		pgmem = rgmem.findall(out)
		gmem = 0.0;
		for x in range(0, len(pgmem), 2):
			gmem = gmem + float(pgmem[x].strip('MiB')) / float(pgmem[x + 1].strip('MiB')) 
		
		info['gmem'] = round(gmem / len(pgmem) * 200, 4)

	# set server name and the protocol id
	info['name'] = config['server_name']
	info['prtc'] = 2
	return json.dumps(info)

class GoatApp():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/var/log/cmaster.log'
        self.stderr_path = '/var/log/cmaster.err'
        self.pidfile_path =  '/var/run/cmaster.pid'
        self.pidfile_timeout = 5
            
    def run(self):
		config = json.loads(open(sys.argv[2]).read())
		while True:
			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			except socket.error as e:
				print(e)
				time.sleep(config['time_sep'])
				continue

			while True:
				msg = collect_info(config)
				if not msg:
					break
				try:
					sock.sendto(msg, (config["master_ip"], config["port"]));
				except Exception as e:
					sock.close()
					print(e)
					break
				time.sleep(config['time_sep'])

if __name__ == "__main__":
	A = GoatApp()
	daemon_runner = runner.DaemonRunner(A)
	daemon_runner.do_action()
