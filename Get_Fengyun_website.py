import urllib
import urllib.parse
import urllib.request
import urllib.error
import requests
import re
import webbrowser
import http.cookiejar
# import json

class Fengyun:
    def __init__(self):
        self.mainUrl='http://satellite.cma.gov.cn/portalsite/default.aspx'
        self.loginUrl='http://satellite.cma.gov.cn/portalsite/WebServ/CommonService.asmx/Login'
        self.loginHeaders={
            'Host': 'satellite.cma.gov.cn',
            'Connection': 'keep-alive',
            'Content-Length': 50,
            'Origin': 'http://satellite.cma.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
            'Content-Type':' application/json;charset=UTF-8',
            'Referer': 'http://satellite.cma.gov.cn/portalsite/default.aspx',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
        }
        #设置cookie
        self.cookie = http.cookiejar.CookieJar()
        #设置cookie处理器
        self.cookieHandler = urllib.request.HTTPCookieProcessor(self.cookie)
        #设置登录时用到的opener，它的open方法相当于urllib2.urlopen
        self.opener = urllib.request.build_opener(self.cookieHandler,urllib.request.HTTPHandler)

    def loginweb(self,userName,userPsw):
        response = self.opener.open(self.mainUrl)
        # 获得验证码
        userCode=self.getcodeID()
        # 验证码信息写入cookie
        cookiee=str('')
        for item in self.cookie:
            cookiee+=str(item.name+'='+item.value+';')
        cookiee+=str('yzmcode='+userCode)
        # cookie写入headers
        self.loginHeaders['Cookies']=cookiee
        # post数据的内容
        postdata=  {
            'userName': userName,
            'userPwd': userPsw,
            'isSave': 'false'
        }
        # 修改编码
        # postencode = urllib.parse.urlencode(postdata)
        # postencodedata = postencode.encode('utf-8')
        response_2 = requests.post(self.mainUrl, data = postdata, headers = self.loginHeaders)
        if response_2.status_code == 200:
            print("成功登陆！")
              #
              # try:
              #     response = self.opener.open(request)
              # except urllib.error.HTTPError as e:
              #     print('The server couldn\'t fulfill the request.')
              #     print('Error code: ', e.code)
              # except urllib.error.URLError as e:
              #     print('We failed to reach a server.')
              #     print('Reason: ', e.reason)
              # else:
              #     print('everything is fine')
              #     #everything is fine
              # content = response.read().decode('utf-8')
              # display = re.compile('<div id=\"BeforeLogin\" class=\"dlcontentdiv\" style=\"(.*?)\">',re.S)
              # itemstodisplay = re.findall(display,content)
              # if itemstodisplay[0]=='display: none;':
              #        print("成功登陆！")


    def getcodeID(self):
        urlweb='http://satellite.cma.gov.cn/portalsite/common/GetCodeImg.aspx'
        webbrowser.open_new(urlweb)
        codeID=input('请输入你的验证码\n>  ')
        return codeID
   #
   # def getUserInfo(self):
   #     urlwebinfo='http://satellite.cma.gov.cn/portalsite/sup/user/ShowUserInfo.aspx'
   #     request = urllib.request.Request(urlwebinfo)
   #     response = urllib.request.urlopen(request)
   #     content = response.read().decode('utf-8')
   #     userInfo = re.compile('<div class=\"grxxnrtext1\">(.*?)</div><div class=\"grxxnrtext2\"><span id=\"Label_General_Type\".*?>(.*?)</span></div>',re.S)
   #     items = re.findall(userInfo, content)
   #     for item in items:
   #         print(item[0]+" : "+item[1]+'\n')


    def main(self,userName,userPsw):
        self.loginweb(userName,userPsw)
        # self.getUserInfo()

userName=input('请输入你的用户名\n>  ')
userPsw=input('请输入你的密码\n>  ')
FYlogin=Fengyun()
FYlogin.main(userName,userPsw)

'''
#说明：
风云网站上的登录方式需要注意！
这个 POST 请求的编码是application/json;charset=UTF-8
参考文献
【1】四种常见的 POST 提交数据方式：https://imququ.com/post/four-ways-to-post-data-in-http.html
【2】登录网页的方法：http://cuiqingcai.com/1076.html
'''
