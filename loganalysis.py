#!/bin/env python
#encoding:utf8

'''
本程序用于统计和分析WEB服务器访问日志，基于python实现。预实现以下功能：

1、 统计独立IP数量											[已完成]
2、 统计PV数量(需要再次请求获取响应类型，比较慢)			[未完成]
3、 统计IP访问量TOP10										[已完成]
4、 统计IP流量TOP10											[已完成]
5、 统计IP502错误TOP10										[已完成]
6、 统计IP503错误TOP10										[已完成]
7、 统计IP504错误TOP10										[已完成]
8、 统计无User-Agent的IP访问TOP10							[已完成]
9、 统计无Referer的IP访问TOP10								[已完成]
10、统计IP各响应码数量										[已完成]
11、统计IP各HTTP协议版本数量								[已完成]
12、统计IP各请求方法数量									[已完成]
----------------------------------
13、统计独立URL数量											[未完成]
14、统计URL访问量TOP10										[未完成]
15、统计URL流量TOP10										[未完成]
16、统计URL502错误TOP10										[未完成]
17、统计URL503错误TOP10										[未完成]
18、统计URL504错误TOP10										[未完成]
19、统计无User-Agent的URL访问TOP10							[未完成]
20、统计无Referer的URL访问TOP10								[未完成]
21、统计URL各响应码数量										[未完成]
22、统计URL各HTTP协议版本数量								[未完成]
23、统计URL各请求方法数量									[未完成]

'''

import sys
import re

# 字典相加
def dictPlus(d1,d2):
	for k,v in d2.iteritems():
		try:
			d1[k] += d2[k]
		except:
			d1[k] = d2[k]
	return d1

def filterKey(Dict,k1,k2):
	list = []
	for k,v in Dict.iteritems():
		try:
			test = v[k1][k2]
			list.append((k,v))
		except:
			pass
	return list

# 日志分析
def analysis(logFile = None, logFileFormat = 'nginx_default'):
	pattern = re.compile(logFormat[logFileFormat])
	IPData = {}
	
	f = open(logFile,'r')
	for i,line in enumerate(f):
		matchs = pattern.match(line)
		if matchs is None:
			print 'not matchd line: %s' % i
			continue
		else:
			_ip, _user, _time, _method, _uri, _proto, _code, _size, _ref, _ua = matchs.groups()
			# begin fill IPData
			if _ua in ('-',''):
				ua_yes_no = 'no'
			else:
				ua_yes_no = 'yes'
			if _ref in ('-',''):
				ref_yes_no = 'no'
			else:
				ref_yes_no = 'yes'
			try:
				test = IPData[_ip]
			except:
				# initialize
				IPData[_ip] = {
						'count':0,
						'size':0,
						'method':{},
						'proto':{},
						'code':{},
						'ref':{'yes':0,'no':0},
						'ua':{'yes':0,'no':0}
				}
			IPData[_ip]['count'] += 1
			IPData[_ip]['size'] += int(_size)
			try:
				IPData[_ip]['method'][_method] += 1
			except:
				IPData[_ip]['method'][_method] = 1
			try:
				IPData[_ip]['proto'][_proto] += 1
			except:
				IPData[_ip]['proto'][_proto] = 1
			try:
				IPData[_ip]['code'][_code] += 1
			except:
				IPData[_ip]['code'][_code] = 1
			IPData[_ip]['ref'][ref_yes_no] += 1
			IPData[_ip]['ua'][ua_yes_no] += 1
			# end fill IPData

	f.close()
	
	TotalItem_IP = len(IPData)
	
	TotalItem_IPCountRank = sorted(IPData.iteritems(),key=lambda i:i[1]['count'],reverse=True)[:10]
	
	TotalItem_IPTrafficRank = sorted(IPData.iteritems(),key=lambda i:i[1]['size'],reverse=True)[:10]
	
	temp = filterKey(IPData,'code','502')
	TotalItem_IPCode502Rank = sorted(temp,key=lambda i:i[1]['code']['502'],reverse=True)[:10]
	
	temp = filterKey(IPData,'code','503')
	TotalItem_IPCode503Rank = sorted(temp,key=lambda i:i[1]['code']['503'],reverse=True)[:10]
	
	temp = filterKey(IPData,'code','504')
	TotalItem_IPCode504Rank = sorted(temp,key=lambda i:i[1]['code']['504'],reverse=True)[:10]
	
	TotalItem_IPNoUserAgentRank = sorted(IPData.iteritems(),key=lambda i:i[1]['ua']['no'],reverse=True)[:10]
	
	TotalItem_IPNoRefererRank = sorted(IPData.iteritems(),key=lambda i:i[1]['ref']['no'],reverse=True)[:10]
	
	TotalItem_CodeCountAndPercent = reduce(dictPlus,[i['code'] for i in IPData.itervalues()])
	
	TotalItem_HTTPVersionAndPercent = reduce(dictPlus,[i['proto'] for i in IPData.itervalues()])
	
	TotalItem_ReqMethodAndPercent = reduce(dictPlus,[i['method'] for i in IPData.itervalues()])
	
	# output to screen
	print '/------------------------------------------------------------'
	print '| 独立IP数量：', TotalItem_IP
	print '\------------------------------------------------------------'
	print
	
	print '/------------------------------------------------------------'
	print '|  IP访问量TOP10：'
	print '|'
	for k,v in TotalItem_IPCountRank:
		print '| ',k,(20-len(k))*' ',v['count']
	print '\------------------------------------------------------------'
	print
	
	print '/------------------------------------------------------------'
	print '|  IP流量TOP10：'
	print '|'
	for k,v in TotalItem_IPTrafficRank:
		print '| ',k,(20-len(k))*' ',v['size']
	print '\------------------------------------------------------------'
	print
	
	print '/------------------------------------------------------------'
	print '|  IP502错误TOP10：'
	print '|'
	for k,v in TotalItem_IPCode502Rank:
		print '| ',k,(20-len(k))*' ',v['code']['502']
	print '\------------------------------------------------------------'
	print
	
	print '/------------------------------------------------------------'
	print '|  IP503错误TOP10：'
	print '|'
	for k,v in TotalItem_IPCode503Rank:
		print '| ',k,(20-len(k))*' ',v['code']['503']
	print '\------------------------------------------------------------'
	print
	
	print '/------------------------------------------------------------'
	print '|  IP504错误TOP10：'
	print '|'
	for k,v in TotalItem_IPCode504Rank:
		print '| ',k,(20-len(k))*' ',v['code']['504']
	print '\------------------------------------------------------------'
	print
	
	print '/------------------------------------------------------------'
	print '|  无User-Agent的IP访问TOP10：'
	print '|'
	for k,v in TotalItem_IPNoUserAgentRank:
		print '| ',k,(20-len(k))*' ',v['ua']['no']
	print '\------------------------------------------------------------'
	print
	
	print '/------------------------------------------------------------'
	print '|  无Referer的IP访问TOP10：'
	print '|'
	for k,v in TotalItem_IPNoRefererRank:
		print '| ',k,(20-len(k))*' ',v['ref']['no']
	print '\------------------------------------------------------------'
	print
	
	print '/------------------------------------------------------------'
	print '|  IP各响应码数量：'
	print '|'
	for k,v in TotalItem_CodeCountAndPercent.iteritems():
		print '| ',k,'  \t',v
	print '\------------------------------------------------------------'
	print
	
	print '/------------------------------------------------------------'
	print '|  IP各HTTP协议版本数量：'
	print '|'
	for k,v in TotalItem_HTTPVersionAndPercent.iteritems():
		print '| ',k,'\t',v
	print '\------------------------------------------------------------'
	print
	
	print '/------------------------------------------------------------'
	print '|  IP各请求方法数量：'
	print '|'
	for k,v in TotalItem_ReqMethodAndPercent.iteritems():
		print '| ',k,(12-len(k))*' ',v
	print '\------------------------------------------------------------'
	print
	
if __name__ == '__main__':
	#nginx default is combined:'$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"';
	#apache default is combined:"%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\""
	logFormat = {
		'nginx_default':r'(?P<ip>\d+\.\d+\.\d+\.\d+) - (?P<user>[^ ]+) [^:]+:(?P<time>[^ ]+) [^ ]+ "(?P<method>[^ ]+) (?P<uri>.+) (?P<proto>HTTP/\d\.\d)" (?P<code>\d+) (?P<size>\d+) "(?P<ref>[^"]*)" "(?P<ua>[^"]*)"\n',
		'apache_default':r'(?P<ip>\d+\.\d+\.\d+\.\d+) [^ ]+ (?P<user>[^ ]+) [^:]+:(?P<time>[^ ]+) [^ ]+ "(?P<method>[^ ]+) (?P<uri>[^ ]+) (?P<proto>HTTP/\d\.\d)" (?P<code>\d+) (?P<size>-|\d+) "(?P<ref>[^"]+)" "(?P<ua>[^"]+)"\n'
	}
	logFile = ''
	logFileFormat = 'nginx_default'
	args = sys.argv
	if len(args) <=1:
		print 'Usage:%s <logfile>' % args[0]
		sys.exit()
	logFile = args[1]
	analysis(logFile = logFile, logFileFormat = logFileFormat)
