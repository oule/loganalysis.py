loganalysis.py
========================

loganalysis.py 是一个通过python语言实现的WEB服务器访问日志统计分析应用。

Version
=======

2013-11-1 发布 loganalysis.py version 1.1 (v1.1)。

Description
===========

* 统计独立IP数量
* 统计IP访问量TOP10
* 统计IP流量TOP10
* 统计IP502错误TOP10
* 统计IP503错误TOP10
* 统计IP504错误TOP10
* 统计无User-Agent的IP访问TOP10
* 统计无Referer的IP访问TOP10
* 统计IP各响应码数量
* 统计IP各HTTP协议版本数量
* 统计IP各请求方法数量

Develop Env
===========

Python 2.6.6  
Centos 6.3

Usage
=====

        ./loganalysis.py </path/to/logfile>
