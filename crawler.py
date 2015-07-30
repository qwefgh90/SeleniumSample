# -*- coding: utf-8 -*-
import requests as rq
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0

import sys,os
from bs4 import BeautifulSoup
hibogo_url="http://hi-bogo.net/"
daum_url="http://www.daum.net"
h_login_url="http://www.hi-bogo.net/cdsb/login_process.php"

#BOARD URL
#LOGIN INFORMATION
h_id = ""
h_passwd = ""
d_id = ""
d_passwd = ""
#hibogo_login function (POST) (mode=login&kinds=outlogin&user_id=qwefgh90&passwd=qwefgh90)
def hibogo_login():
    post_bd = {'mode':'login','kinds':'outlogin','user_id':h_id,'passwd':h_passwd}
    rs = rq.post(h_login_url,data = post_bd)
    h =rs.headers
    print h
    #c = rs.content
    #a=open('afterlogin.html','wb');a.write('<!DOCTYPE html><head><meta charset=\"utf-8\"></head>');a.write(c);a.close()
    cookie_str = h['set-cookie']	#login session
    return cookie_str

def hibogo_login2():
    driver = webdriver.PhantomJS()
    driver.get(hibogo_url)
    driver.set_window_size(1024, 768)
    driver.find_element_by_name("user_id").send_keys(h_id)
    driver.find_element_by_name("passwd").send_keys(h_passwd)
    login_button = driver.find_element_by_id("lx")
    login_button.click()

    driver.get(hibogo_url)
    driver.save_screenshot('hibogo_login.png')
    cookies = {}
    for cookie in driver.get_cookies():
        print "%s -> %s" % (cookie['name'], cookie['value'])
        cookies[cookie['name']] = cookie['value']
    return cookies

def daum_login():
    driver = webdriver.PhantomJS()
    driver.get(daum_url)
    driver.set_window_size(1024,768)
    idinput = driver.find_element_by_id("id")
    idinput.send_keys(d_id)
    driver.find_element_by_id("inputPwd").send_keys(d_passwd)
    driver.save_screenshot('daum_before_login.png')
    login_button = driver.find_element_by_id("loginSubmit")
    login_button.click()
    idinput.submit()
#	wait = WebDriverWait(driver, 5)
#	try:
#   		element = wait.until(EC.presence_of_element_located((By.ID, "daum")))
#	except:
#		print 'except occur'
#	finally:
#		pass
    driver.save_screenshot('daum_before_login2.png')
    driver.get(daum_url)
    driver.save_screenshot('daum_login.png')
    driver.get("http://mail2.daum.net/hanmailex/Top.daum?")
    driver.save_screenshot('daum_mail.png')

naver_url = 'http://www.naver.com'
naver_id = ''
naver_passwd = ''
def naver_login():
    #executable_path에 PhantomJS 실행 경로 입력 (필수아님)
    driver = webdriver.PhantomJS(executable_path='/Users/cheochangwon/Documents/WorkspacePython/SeleniumSample/phantomjs'
    , service_args=['--ssl-protocol=tlsv1'])
    #인증서 관련 업데이트
    #'--ignore-ssl-errors=true',
    #https://groups.google.com/forum/#!topic/nzpug/Y2UfnQcG7YU
    #http://stackoverflow.com/questions/12021578/phantomjs-failing-to-open-https-site
    driver.get(naver_url)
    driver.set_window_size(1024,768)
    naver_login_frame = driver.find_element_by_id("loginframe")
    driver.switch_to_frame(naver_login_frame)
    idinput = driver.find_element_by_id("id")
    idinput.send_keys(naver_id)
    idinput = driver.find_element_by_id("pw")
    idinput.send_keys(naver_passwd)
    driver.save_screenshot('naver_before_login.png')
    inputs = driver.find_elements_by_xpath('//input')
    input = None
    print '[SEARCHING]'
    for element in inputs:
        value = element.get_attribute('value')
        title = element.get_attribute('title')
        if (value == u'로그인') and (title == u'로그인'):
            input = element
            print '[FINDED] ELEMENT'
            break
    driver.find_element_by_id('ckb_type').click();  #보안 로그인 OFF
    input.click()
    print '[CLICK & WAITING]'
    driver.save_screenshot('naver_after_login.png')

if __name__ == '__main__':
    # hibogo_login2();
    # sys.exit();
    naver_login()
    sys.exit()
    cookies = hibogo_login2()
    anchor_list = hibogo_getboard(cookies)
    hibogo_crawl(cookies,anchor_list)
    with open('hibogo_crawl.json','wb') as f:
        import json
        json.dump(anchor_list,f,ensure_ascii=False,encoding='utf-8')
