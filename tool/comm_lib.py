from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

import time

from conf import config
from tool.enum_instance import Order


# 一些通用依赖


def move_down(driver: webdriver):
    """
    下滑动作
    """
    time.sleep(1)
    bg = driver.find_element_by_css_selector('body')
    bg.send_keys(Keys.SPACE)


def page_up(driver: webdriver):
    """
    翻页
    """
    while True:
        try:
            tag = driver.find_element_by_css_selector(Order.page_down.value)
            if tag:
                time.sleep(2)
                tag.click()
                break
        except ElementClickInterceptedException:
            move_down(driver)


def into_live(driver: webdriver):
    """
    进入直播页面,标签页面可变更
    """
    driver.find_element_by_link_text(u"直播").click()


def time_spend(func):
    def wrapper(*args, **kwargs):
        local_time = time.time()
        func(*args, **kwargs)
        print('耗时 「{}」'.format(time.time() - local_time))
    return wrapper


def _add_cookies(driver: webdriver):
    """
    设置 cookies
    """
    if len(config.cookies) == 0:
        raise TypeError("cookies 为空")

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
            driver.add_cookie(d)
    driver.refresh()


def driver_option():
    service_args = list()
    # service_args.append("--headless")
    service_args.append('--load-images=no')          # 关闭图片加载,关闭图片加载有蜜汁BUG
    service_args.append('--disk-cache=yes')          # 开启缓存
    service_args.append('--ignore-ssl-errors=true')  # 忽略https错误
    driver = webdriver.Chrome(service_args=service_args)
    return driver
