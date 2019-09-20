import threading
from typing import List
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import time

from pyquery import PyQuery as pq
from tool.comm_lib import driver_option, into_live, _add_cookies
from tool.enum_instance import Order


def page_down(driver: webdriver):
    """
    下滑动作
    """
    time.sleep(3)
    # bg = driver.find_element_by_css_selector('body')
    # bg.send_keys(Keys.SPACE)
    # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    # ActionChains(driver).move_by_offset(200, 100).click().perform()  # 鼠标左键点击， 200为x坐标， 100为y坐标
    ActionChains(driver).double_click()
    driver.send_keys(Keys.CONTROL, Keys.ARROW_DOWN)


def page_up():
    """
    测试翻页
    """
    driver = driver_option()
    driver.maximize_window()

    url = 'https://www.huya.com/l'
    driver.get(url)
    driver.implicitly_wait(10)
    driver.refresh()

    href_list = []

    while True:
        try:
            tag = driver.find_element_by_css_selector(Order.page_down.value)
            if tag:
                tag.click()
                time.sleep(3)
                pg, sum = get_source(driver)
                source_from_page(pg, sum, href_list)
        except ElementClickInterceptedException:
            return href_list
        except NoSuchElementException:
            print("---here---")
            page_down(driver)
            time.sleep(3)


def get_source(driver: webdriver):
    sum_room = driver.find_elements_by_class_name(Order.room_tag.value)
    try:
        tag = driver.find_element_by_css_selector(Order.page_down.value)
        if tag:
            pg = driver.page_source
            return pg, len(sum_room)
    except NoSuchElementException:
        page_down(driver)


def source_from_page(page: str, sum: int, url_list: List[str]) -> List[str]:
    """
    从 url 中下载网页并解析出页面内所有的电影
    """
    e = pq(page)
    i = 0
    while i < sum:
        items = e('#js-live-list > li:nth-child({}) > a.video-info.new-clickstat'.format(i+1)).attr('href')
        url_list.append(items)
        i += 1
    return url_list


def driver_init(href: str):
    """
    初始化
    """
    # 初始化 webdriver
    driver = driver_option()

    driver.get(href)
    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.refresh()

    # 设置 cookies
    _add_cookies(driver)

    return driver


def auto_receive_href():
    pass


def chrome_option_cookies():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.maximize_window()
    return browser


def test_main():
    # --------- 测试获取 html 源码----------
    driver = driver_option()
    driver.get("https://www.huya.com/l")
    driver.maximize_window()
    driver.implicitly_wait(5)

    _add_cookies(driver)
    into_live(driver)
    # 获取页面源码
    resp, num = get_source(driver)
    lst = []
    result = source_from_page(resp, num, lst)

    r1 = result[:60]
    print(r1, len(r1))

    r2 = result[60:]
    print(r2, len(r2))

    # --------- 测试 多线程任务锁 ---------
    # log_int_thread()
    # -------- 测试 多线程全局变量 --------
    # thread_func_global()

    # -------- 测试不停翻页 ---------
    # resp = page_up()
    # print(resp)

    # 测试启用 Chrome option 启动，phantomjs 需要做反爬虫
    # driver = chrome_option_cookies()
    # driver.get("https://www.huya.com/l")
    # _add_cookies(driver)
    # time.sleep(10)
    pass


if __name__ == '__main__':
    test_main()
