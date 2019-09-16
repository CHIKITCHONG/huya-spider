from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


# def test_into_room():
#     """
#     进入房间功能
#     """
#     browser = webdriver.Chrome()
#     url = 'https://www.huya.com/l'
#
#     browser.get(url)
#     time.sleep(5)
#
#     browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
#
#     time.sleep(5)
#     button = browser.find_elements_by_id('//*[@id="js-live-list"]/li[2]')
#     button.click()
#     time.sleep(10)
#     browser.close()
#
#
# def test2_select_room():
#     """
#     房间号选择
#     #js-live-list > li:nth-child(1) > a.title.new-clickstat
#     """
#     browser = webdriver.Chrome()
#
#     try:
#
#         browser.get('http://huya.com/l')
#
#         # 滑动至底部
#         js = "var q=document.documentElement.scrollTop=100000"
#         browser.execute_script(js)
#         time.sleep(10)
#
#         # 寻找房间
#         sum = browser.find_element_by_css_selector("#js-live-list > li:nth-child(2) > a.video-info.new-clickstat")
#         sum.click()
#
#         # 暂停100
#         time.sleep(100)
#
#     finally:
#         browser.close()


def test_handle_cookies():
    """
    处理 cookies
    """
    d = {}
    cookies = """Hm_lvt_51700b6c722f5bb4cf39906a596ea41f=1566188187,1566375475,1567417273,1568079813; __yasmid=0.6390285896314234; __yamid_tt1=0.6390285896314234; __yamid_new=C8981998585000017D551C70DE821EF0; udb_passdata=3; SoundValue=0.50; alphaValue=0.80; guid=b73e698be403775d8c48b107b2073864; udb_guiddata=5b34f97b40b948bc8b3958191c35bf54; web_qrlogin_confirm_id=083ce166-a475-49fe-a6a1-a8463c908861; udb_accdata=13559775273; PHPSESSID=jovhe82qe9p7cedq5p86a0okf7; udb_biztoken=AQB2pgZoqAb5IycoAkmOZWJWxk7UTHqNec7dMF2lxsSZh1AraMSX_H_8_Gfc2WRKbsrdPA2QKEA8iV8PgxZAtwN1rOt6O2whNeTs9c-kgKFlZIMCof_8e6E4_69WeMSXKAhUb7wjTP8ahBsiSgOWdXqQTXm2FDgpD2xTJq9Vmg19DIiI_eIfXlhQJ8OJCb9wRxyyqfE9JOMVXRUuUM9L07tndTFo9BzkuAZ_RdBCllR7lRWtz7t9kFdI3N86qjIM2ik9wYLhvU-vKGdlSjFgf7l5cLCGMQTqvlT69iKnVsxNRjVQVVhrgB9sECT_tDmOcDJyZvzHQoLUByxTDQrzqY-D; udb_origin=1; udb_other=%7B%22lt%22%3A%221568167961107%22%2C%22isRem%22%3A%221%22%7D; udb_passport=hy_25273396; udb_status=1; udb_uid=1199522243690; udb_version=1.0; username=hy_25273396; yyuid=1199522243690; h_unt=1568167962; __yaoldyyuid=1199522243690; _yasids=__rootsid%3DC8986CB1A4F000012AE9233017B31647; isInLiveRoom=; Hm_lpvt_51700b6c722f5bb4cf39906a596ea41f=1568168067"""
    res = cookies.split(';')
    for i in res:
        # key, value = i.split('=')[0], i.split('=')[1]
        key, value = i.split('=', 1)
        d[key] = value
    return d


# def test_browser_login():
#     """
#     进入登陆页面并完成登陆  success
#     """
#     browser = webdriver.Chrome()
#     url = 'https://www.huya.com/'
#
#     browser.get(url)
#     browser.implicitly_wait(10)
#     browser.refresh()
#
#     # 账号
#     browser.find_element_by_id("nav-login").click()
#     browser.switch_to_frame("UDBSdkLgn_iframe")
#     try:
#         # browser.find_element_by_class_name("udb-input udb-input-account")
#         browser.find_element_by_css_selector("#account-login-form > div:nth-child(1) > input").send_keys("13559775273")
#         browser.find_element_by_css_selector("#account-login-form > div:nth-child(2) > input").send_keys("zqf20101208")
#         time.sleep(3)
#         browser.find_element_by_css_selector("#account-login-form > div:nth-child(7)").click()
#         time.sleep(30)
#
#     except Exception as e:
#         print(browser.page_source)
#
#     browser.close()


# def test_into_zhibo():
#     """
#     完成登陆并进入全部直播页面, success
#     """
#     browser = webdriver.Chrome()
#     url = 'https://www.huya.com/'
#
#     browser.get(url)
#     browser.implicitly_wait(10)
#     browser.refresh()
#
#     # 账号
#     browser.find_element_by_id("nav-login").click()
#     browser.switch_to_frame("UDBSdkLgn_iframe")
#     try:
#         # browser.find_element_by_class_name("udb-input udb-input-account")
#         browser.find_element_by_css_selector("#account-login-form > div:nth-child(1) > input")
#         .send_keys("13559775273")
#         browser.find_element_by_css_selector("#account-login-form > div:nth-child(2) > input")
#         .send_keys("zqf20101208")
#         time.sleep(3)
#         browser.find_element_by_css_selector("#account-login-form > div:nth-child(7)").click()
#         time.sleep(30)
#
#     except Exception as e:
#         print(browser.page_source)
#
#     try:
#         browser.find_element_by_link_text(u"直播").click()
#     except Exception as e:
#         raise ValueError("点直播时出错")
#
#     browser.close()


# def test_into_room():
#     """
#     进入多个直播页面
#
#     #js-live-list
#     """
#     browser = webdriver.Chrome()
#     url = 'https://www.huya.com/l'
#     browser.get(url)
#     browser.implicitly_wait(10)
#     browser.refresh()
#
#     # js = "var q=document.documentElement.scrollTop=10000"
#     # browser.execute_script(js)
#     """laypage_btn
#        #laypage_0 > span.laypage_total > button
#     """
#     try:
#         browser.find_elements_by_css_selector("#laypage_0 > span.laypage_total > button")
#         print("----tool----")
#     except Exception as e:
#         bg = browser.find_element_by_css_selector('body')
#         bg.send_keys(Keys.SPACE)
#     time.sleep(10)
#     browser.close()


# def test_move_down():
#     driver = webdriver.Chrome()
#     url = 'https://www.huya.com/l'
#     driver.get(url)
#     driver.implicitly_wait(10)
#     driver.refresh()
#
#     driver.maximize_window()
#     driver.execute_script("window.scrollBy(0,3000)")
#     time.sleep(1)
#     driver.execute_script("window.scrollBy(0,5000)")
#     time.sleep(1)


def page_down(driver: webdriver):
    """
    下滑动作
    """
    bg = driver.find_element_by_css_selector('body')
    bg.send_keys(Keys.SPACE)


def test_page_up():
    """
    测试翻页
    """
    driver = webdriver.Chrome()
    url = 'https://www.huya.com/l'
    driver.get(url)
    driver.implicitly_wait(10)
    driver.refresh()

    # while True:
    #     try:
    #         tag = driver.find_element_by_css_selector("#laypage_0 > a.laypage_next")
    #         if tag:
    #             time.sleep(10)
    #             tag.click()
    #             time.sleep(5)
    #             break
    #     except Exception as e:
    #         print("--- tool ---")
    #         page_down(driver)

    while True:
        try:
            tag = driver.find_element_by_css_selector("#laypage_0 > a.laypage_next")
            if tag:
                time.sleep(10)
                tag.click()
                time.sleep(5)
                break
        except ElementClickInterceptedException:
            page_down(driver)


if __name__ == '__main__':
    # test_into_room()
    # test_handle_cookies()
    # test_browser_login()
    # test_into_zhibo()
    # test_into_room()
    # test_move_down()
    test_page_up()
