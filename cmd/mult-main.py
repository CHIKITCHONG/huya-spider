import multiprocessing
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq
import time

from conf import config
from tool.comm_lib import driver_option, _add_cookies, time_spend, move_down
from tool.enum_instance import Order
from tool.until import log


def driver_init(href: str):
    """
    初始化
    """
    # 初始化 webdriver
    driver = driver_option()

    driver.get(href)
    driver.maximize_window()
    driver.implicitly_wait(5)

    # 设置 cookies
    _add_cookies(driver)

    return driver


def task():
    pass


def get_source():
    driver = driver_init('https://www.huya.com/l')

    sum_room = driver.find_elements_by_class_name(Order.room_tag.value)
    try:
        tag = driver.find_element_by_css_selector(Order.page_down.value)
        if tag:
            pg = driver.page_source
            return pg, len(sum_room)
    except NoSuchElementException:
        move_down(driver)


def source_from_page(page: str, sum: int):
    """
    从 url 中下载网页并解析出页面内所有的电影
    """
    e = pq(page)
    href_list = []
    i = 0
    while i < sum:
        items = e('#js-live-list > li:nth-child({}) > a.video-info.new-clickstat'.format(i+1)).attr('href')
        href_list.append(items)
        i += 1
    return href_list


def room_handle(href: str):
    """
    一个主处理函数处理进入房间发评论
    """
    driver = driver_init(href)
    try:
        # 等待页面加载完成
        element = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, Order.send_button.value))
        )
        time.sleep(1)

        # driver.implicitly_wait(5)
        if element:
            tag = driver.find_element_by_css_selector(Order.comment.value)
            tag.send_keys(config.content)
            # 发送成功写入日志
            # log('normal [在房间 {} 发送了: {}]'.format(room_title, config.content))
            time.sleep(1)
            tag.send_keys(Keys.ENTER)
            driver.find_element_by_css_selector(Order.send_button.value).click()
            time.sleep(1)

    except Exception as e:
        log('error ', e)
        raise ZeroDivisionError("发送评论标签有变导致 selenium 定位出错，请修正")

    driver.close()


@time_spend
def main(href_lift):

    href_list = ['https://www.huya.com/chuhe', 'https://www.huya.com/518512', 'https://www.huya.com/518518', 'https://www.huya.com/12323', 'https://www.huya.com/pp1204', 'https://www.huya.com/edc595', 'https://www.huya.com/shangjin', 'https://www.huya.com/pcl', 'https://www.huya.com/131499', 'https://www.huya.com/125393', 'https://www.huya.com/wjz520cx', 'https://www.huya.com/417964', 'https://www.huya.com/saonan', 'https://www.huya.com/408604', 'https://www.huya.com/52616', 'https://www.huya.com/229085', 'https://www.huya.com/lpl', 'https://www.huya.com/agbaozi', 'https://www.huya.com/592655', 'https://www.huya.com/159409', 'https://www.huya.com/housangun', 'https://www.huya.com/godv', 'https://www.huya.com/100953', 'https://www.huya.com/11342412', 'https://www.huya.com/111288', 'https://www.huya.com/588332', 'https://www.huya.com/616702', 'https://www.huya.com/qingwa666', 'https://www.huya.com/11352908', 'https://www.huya.com/14734090', 'https://www.huya.com/920314', 'https://www.huya.com/107222', 'https://www.huya.com/hujiangjun', 'https://www.huya.com/liushaji', 'https://www.huya.com/18618316', 'https://www.huya.com/nest2019', 'https://www.huya.com/baozha', 'https://www.huya.com/400298', 'https://www.huya.com/11342421', 'https://www.huya.com/402958', 'https://www.huya.com/gushouyu', 'https://www.huya.com/baby25', 'https://www.huya.com/daomeili', 'https://www.huya.com/501781', 'https://www.huya.com/428354', 'https://www.huya.com/bg90010abl', 'https://www.huya.com/475974', 'https://www.huya.com/dasdad', 'https://www.huya.com/11342390', 'https://www.huya.com/521715', 'https://www.huya.com/guanzongo', 'https://www.huya.com/678398', 'https://www.huya.com/503376', 'https://www.huya.com/hunterxw', 'https://www.huya.com/520214', 'https://www.huya.com/52503', 'https://www.huya.com/miss', 'https://www.huya.com/longdd', 'https://www.huya.com/11352970', 'https://www.huya.com/14983601', 'https://www.huya.com/captain', 'https://www.huya.com/qiguaijun', 'https://www.huya.com/712722', 'https://www.huya.com/11352915', 'https://www.huya.com/734081', 'https://www.huya.com/huanxiongjun', 'https://www.huya.com/chenxi6', 'https://www.huya.com/cxldb', 'https://www.huya.com/chushouguai', 'https://www.huya.com/284931', 'https://www.huya.com/742611', 'https://www.huya.com/chaojie', 'https://www.huya.com/19516286', 'https://www.huya.com/991202', 'https://www.huya.com/951058', 'https://www.huya.com/wangshi520', 'https://www.huya.com/nanyanx', 'https://www.huya.com/528364', 'https://www.huya.com/lck', 'https://www.huya.com/12130732', 'https://www.huya.com/kpl', 'https://www.huya.com/5801xiaowei', 'https://www.huya.com/11336571', 'https://www.huya.com/ximen', 'https://www.huya.com/17635616', 'https://www.huya.com/mifengaaa', 'https://www.huya.com/742610', 'https://www.huya.com/880215', 'https://www.huya.com/981585', 'https://www.huya.com/842782', 'https://www.huya.com/yuanwang', 'https://www.huya.com/966988', 'https://www.huya.com/daleilei', 'https://www.huya.com/18015095', 'https://www.huya.com/10193973', 'https://www.huya.com/clkimmy', 'https://www.huya.com/520320', 'https://www.huya.com/11352944', 'https://www.huya.com/52398', 'https://www.huya.com/19277670', 'https://www.huya.com/761792', 'https://www.huya.com/11352914', 'https://www.huya.com/494680', 'https://www.huya.com/11947428', 'https://www.huya.com/590935', 'https://www.huya.com/11342396', 'https://www.huya.com/102491', 'https://www.huya.com/970711', 'https://www.huya.com/937430', 'https://www.huya.com/990424', 'https://www.huya.com/637829', 'https://www.huya.com/sunshen', 'https://www.huya.com/liuxingyu', 'https://www.huya.com/mozimeng', 'https://www.huya.com/513533', 'https://www.huya.com/17278481', 'https://www.huya.com/dracula', 'https://www.huya.com/18553978', 'https://www.huya.com/539497', 'https://www.huya.com/luolijiang']

    p = multiprocessing.Pool(processes=3)

    for i in range(len(href_list)):
        p.apply_async(room_handle, (href_list[i], ))

    p.close()
    p.join()


if __name__ == '__main__':
    main()
