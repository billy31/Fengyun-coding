# -*- coding: UTF-8 -*-
import requests
import webbrowser
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib
import time
from os.path import join

class fengyun:
    def __init__(self):
        self.response = requests.session()
        # self.web_js = webdriver.Chrome()
        self.web_js = webdriver.PhantomJS()
        self.mainUrl = 'http://satellite.cma.gov.cn/portalsite/default.aspx'
        self.loginUrl = 'http://satellite.cma.gov.cn/portalsite/WebServ/CommonService.asmx/Login'
        self.codeurl = 'http://satellite.cma.gov.cn/portalsite/common/GetCodeImg.aspx'
        self.userinfo = 'http://satellite.cma.gov.cn/portalsite/sup/user/ShowUserInfo.aspx'
        self.check = 'http://satellite.cma.gov.cn/PortalSite/Ord/MyOrders.aspx'
        self.search = 'http://satellite.cma.gov.cn/PortalSite/Data/Satellite.aspx'
        self.shoppingcart = 'http://satellite.cma.gov.cn/PortalSite/Data/ShoppingCart.aspx'
        self.loginHeaders = {
            'Host': 'satellite.cma.gov.cn',
            'Connection': 'keep-alive',
            'Content-Length': 50,
            'Origin': 'http://satellite.cma.gov.cn',
            'User-Agent': 'python-requests/2.10.0',
            'Content-Type':' application/json;charset=UTF-8',
            'Referer': 'http://satellite.cma.gov.cn/portalsite/default.aspx',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        }

    def getcodeid(self):
        webbrowser.open_new_tab(self.codeurl)
        codeID=raw_input('请输入验证码 \n>  ')
        return codeID

    def login(self, name, pswd):
        content=self.response.get(self.mainUrl)
        cookiestopost={}
        for items in self.response.cookies:
            cookiestopost[items.name]=items.value
        code = self.getcodeid()
        cookiestopost['yzmcode']=code
        cookie = json.dumps(cookiestopost)
        self.loginHeaders['Cookie']=cookie
        payload = {}
        payload={'userName':name,'userPwd':pswd,'isSave':'true'}
        page = self.response.post(self.loginUrl,data=json.dumps(payload),headers=self.loginHeaders)
        # webbrowser.open_new_tab(self.mainUrl)
        self.web_js.get(self.mainUrl)
        cookie_dict = {}
        for x in self.response.cookies:
            cookie_dict['name'] = x.name
            cookie_dict['value'] = x.value
            self.web_js.add_cookie(cookie_dict)
        self.web_js.get(self.mainUrl)

    def summitorder(self):
        # print  save_cookie
        select_one_file='http://satellite.cma.gov.cn/PortalSite/WebServ/CommonService.asmx/selectOne'
        postdata1 = {'filename': 'FY3C_VIRRX_GBAL_L1_20160510_1445_1000M_MS.HDF',
                              'ischecked': 'true',  'satellitecode': 'FY3C',  'datalevel': 'L1'}

        midpage = self.response.post(select_one_file, data=json.dumps(postdata1),headers=self.loginHeaders)
        # print midpage.headers
        cookiesX = {}
        for cookiesXx in midpage.cookies:
            cookiesX[cookiesXx.name] = cookiesXx.value
        new_headers = {
            'Accept': 'application/json,text/javascript,*/*;q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection':'keep-alive',
            'Content-Length': 0,
            'Content-Type':' application/json;charset=UTF-8',
            'Host':'satellite.cma.gov.cn',
            'Origin':'http://satellite.cma.gov.cn',
            'Referer':'http://satellite.cma.gov.cn/PortalSite/Data/FileShow.aspx',
            'User-Agent': 'python-requests/2.10.0',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': cookiesX
        }
        bind = 'http://satellite.cma.gov.cn/PortalSite/WebServ/CommonService.asmx/BindShowCartInfo'
        bind_cart = self.response.post(bind, headers=new_headers)
        # print bind_cart.headers

        url_to_check = 'http://satellite.cma.gov.cn/PortalSite/Data/ShoppingCart.aspx'
        check_page = self.response.get(url_to_check)

        check_soup = BeautifulSoup(check_page.text,'html.parser')
        check_page_content = check_soup.find('div',class_='gwcrightcontentimg2')
        for items in check_page_content:
            print items
            print '****************************************************'

        # submit it
        submit_file = 'http://satellite.cma.gov.cn/PortalSite/WebServ/CommonService.asmx/Submit'
        postdata2 = {'hkIsPushMode': 'false', 'chkIsSendMail': 'false', 'radioBtnlist_ftp': '0'}
        finpage = self.response.post(submit_file, data=json.dumps(postdata2))
        print finpage

    def searchproducts_js(self):
        self.web_js.get(self.search)
        time.sleep(2)
        # instrument and products
        instrument = 'VIRR'
        self.web_js.find_element_by_id(instrument).click()
        level = 'L1'
        self.web_js.find_element_by_xpath('//*[@id="divImg'+level+'"]/img').click()
        time.sleep(2)
        # self.web_js.find_element_by_xpath('//*[@id="ckAll"]').clear()
        self.web_js.find_element_by_xpath('//*[@id="ckAll"]').click()
        #if all_check.is_selected() != 'False':

        # time
        begin_date = '2016-05-20'
        beginD = self.web_js.find_element_by_id('txtBeginDate')
        beginD.clear()
        beginD.send_keys(begin_date)

        end_date = '2016-05-23'
        endD = self.web_js.find_element_by_id('txtEndDate')
        endD.clear()
        endD.send_keys(end_date)

        # area
        cover = 'rdAllCover'
        self.web_js.find_element_by_xpath('//*[@id="'+cover+'"]').click()
        # part area temporarily
        self.web_js.find_element_by_xpath('//*[@id="rdbj"]').click()

        #search
        self.web_js.find_element_by_xpath('//*[@id="imgSearch"]').click()

    def choose_files_js(self):
        self.web_js.switch_to.window(self.web_js.window_handles[-1])
        time.sleep(3)
        self.web_js.find_element_by_xpath('//*[@id="imgSelectAll2"]').click()
        # self.web_js.find_element_by_xpath('//*[@id="form1"]/div[3]/div[4]/div/div[8]/a/img').click()
        time.sleep(5)
        self.web_js.get(self.shoppingcart)

    def checkorders(self):
        print "\n*******************************************\n"
        check_order=self.response.get(self.check)
        # print check_order
        soup = BeautifulSoup(check_order.text,'html.parser')
        # contents = soup.findAll('tr',class_='plantload')
        # contents = soup.findAll('div', id='divDisplayOrdersList')
        # error = soup.find('div',class_='loginnr3')
        testing = webdriver.Chrome()
        newcookie={}
        for item in self.response.cookies:
            newcookie[item.name]=item.value
            print item.name+' : '+item.value+'\n'
            testing.add_cookie({item.name:item.value})

        testing.get(self.check)
        b = testing.find_element_by_class_name('plantload')
        print b
        print '{ \n'
        # print error
        print '} \n'
        print "*******************************************\n"
        print 'OrderList: \n'
        # for items in contents:
        #   print items
        '''
        '''

    def checkorders_2(self):
        # print pq(self.check)
        check_order_content = self.response.get(self.check)
        '''
        cookies = {}
        for item in self.response.cookies:
            cookies['name'] = item.name
            cookies['value'] = item.value
            cookies['domain'] = item.domain
        a = webdriver.Chrome()
        a.add_cookie(cookies)
        a.get(self.check)

        handler = urllib2.HTTPCookieProcessor(cookies)
        opener = urllib2.build_opener(handler)
        result = opener.open(self.check)

        '''
        filepath = "E:\\"
        filename = "testing.txt"
        urllib.urlretrieve(self.check, join(filepath, filename))
        # with open(join(filepath, filename), 'wb') as f:
        #   f.write(check_order_content)
        content = open(filepath+filename)
        text = content.read()
        soup = BeautifulSoup(text, 'html.parser')
        contents = soup.findAll('tr', class_='plantload')
        for item in contents:
            print item
            print "******************************************************************"

    def checkorders_js(self):
        # shopping carts
        self.web_js.switch_to.window(self.web_js.window_handles[-1])
        time.sleep(1)
        soup = BeautifulSoup(self.web_js.page_source,'html.parser')
        username = soup.find_all('span',id='lblUserName')
        filecounts = soup.find_all('span',id='lblFileCount')
        filesize = soup.find_all('span', id='lblFileSize')
        print username[0].string,
        print ',当前购物车中共有'
        print filecounts[0].string,
        print '个文件，大小',
        print filesize[0].string
        # self.web_js.find_element_by_xpath('//*[@id="imgSubmit"]').click()

        # orders
        self.web_js.get(self.check)
        time.sleep(1)
        list = self.web_js.find_elements_by_class_name('plantload')
        for item in list:
            if item.text != '':
                print item.text

    def testing(self):
        isLogin=self.response.get(self.mainUrl)
        soup = BeautifulSoup(isLogin.text,'html.parser')
        finds = soup.find('label',id='lblName')
        print finds
        namexxx = soup.find('div', id='AfterLogin')['style']
        print namexxx

    def main(self,name, pswd):
        self.login(name, pswd)
        time.sleep(2)
        self.searchproducts_js()
        time.sleep(5)
        self.choose_files_js()
        # time.sleep(5)
        self.checkorders_js()

        print 'finished'
        # self.summitorder()
        # self.checkorders()
        # self.checkorders_2()

name = raw_input('username \n>  ')
pswd = raw_input('password \n>  ')
fy = fengyun()
fy.main(name, pswd)
