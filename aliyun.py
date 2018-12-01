import urllib2
import itchat

url = "http://www.kanter.cn/ip.html"

req = urllib2.Request(url)
res_data = urllib2.urlopen(req)
res = res_data.read()

itchat.auto_login(hotReload=True, enableCmdQR=2)
itchat.send("today IP:"+res , toUserName='filehelper')

print res





