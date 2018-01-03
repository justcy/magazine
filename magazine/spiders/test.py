#-*- coding:utf8 -*-
str = '你好2014-08-03'
# str =  str.decode('utf-8')[0:1].encode('utf-8')
str = str.replace('好',"-").replace('你',"asdf-")
print str