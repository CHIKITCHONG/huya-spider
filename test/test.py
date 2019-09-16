from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from conf import config


def handle_cookies():
    """
    处理 cookies
    """
    d = {}
    cookies = """SoundValue=0.50; __yamid_tt1=0.6458637742000024; __yamid_new=C8992A46FAC000019C7B16D4192F68E0; alphaValue=0.80; guid=0e74b06dae607b5d1936fde8fee872a7; udb_guiddata=199955810db54b2d908be00902d5411a; udb_accdata=13559775273; avatar=http://thirdwx.qlogo.cn/mmopen/vi_32/nT8M2ziaETBkTTuVIvpM40eHPHI2VEOcT8zrMwnsJox4ZCrcb7GYe2LUZblxwGquzgpibsLkoToPZWkau3mHQPibQ/132; nickname=ZI%E6%9D%B0; partner_uid=op55owhf8IXPDbRC--NJ8gjRt530; udb_biztoken=AQBrQXo90rIew3HjbqUuXLX2Scr-8BPlj1XqK8x6tC8KFrjaaJujPXpkyBLTQpmqpHUL5ekoPoh11bSEsfOX9ogNorkCji1g4-KsqlAqmG_fWV4YIafJOzP0DMFJl36joQkdDArEejl58-w_PfUoxXuWD00FXC1O1chg5niWur32NaTexVFotXC1kAvMV8QxDJ2EpspVVc7IxqNFUOP50SzvULdZiKwxdhJrbBbXbbufRZXEcYGSN_mMA_qqGVSj3tXqYdhVKBaLuQ4WGdT_sSUMwCY08lasGfmdEd45RnHvqO4V0q0jpCQUudYf9iWGNcNHri-2pmdyw1WJwlIMVLwR; udb_openid=op55owhf8IXPDbRC--NJ8gjRt530; udb_origin=100; udb_other=%7B%22lt%22%3A%221568607449502%22%2C%22isRem%22%3A%221%22%7D; udb_passport=qq_hyajbx8923j7; udb_status=1; udb_uid=2284177747; udb_version=1.0; username=qq_hyajbx8923j7; yyuid=2284177747; lType=weixin; PHPSESSID=ud39bs4f4ic0bv29ljp79gtf74; h_unt=1568625990; Hm_lvt_51700b6c722f5bb4cf39906a596ea41f=1568532382,1568559447,1568606763,1568625991; __yasmid=0.6458637742000024; __yaoldyyuid=2284177747; _yasids=__rootsid%3DC89A217FEF80000166291E167A0011E2; udb_passdata=3; isInLiveRoom=; Hm_lpvt_51700b6c722f5bb4cf39906a596ea41f=1568629007"""
    res = cookies.split(';')
    for i in res:
        # key, value = i.split('=')[0], i.split('=')[1]
        key, value = i.split('=', 1)
        d[key] = value
    return d


def page_down(driver: webdriver):
    """
    下滑动作
    """
    bg = driver.find_element_by_css_selector('body')
    bg.send_keys(Keys.SPACE)


def page_up():
    """
    测试翻页
    """
    driver = webdriver.Chrome()
    url = 'https://www.huya.com/l'
    driver.get(url)
    driver.implicitly_wait(10)
    driver.refresh()

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


def _add_cookies():
    """
    测试添加 cookies, success
    """
    driver = webdriver.Chrome()
    url = 'https://www.huya.com/'
    driver.get(url)
    driver.implicitly_wait(10)
    driver.refresh()

    for part in config.cookies.split('; '):
        k, v = part.split('=', 1)
        if driver.get_cookie(k) is None:
            d = dict(
                name=k,
                value=v,
                path='/',
                domain='.huya.com',
                secure=False
            )
            # print('cookie', d)
            driver.add_cookie(d)
    driver.get('https://www.huya.com/l')
    time.sleep(50)


def test_main():
    _add_cookies()


if __name__ == '__main__':
    test_main()
