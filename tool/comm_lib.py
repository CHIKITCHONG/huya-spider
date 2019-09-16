from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

import time

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
