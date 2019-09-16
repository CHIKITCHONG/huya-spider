from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import time

from tool.comm_lib import move_down, into_live, time_spend
from tool.enum_instance import Order
from conf import config
from tool.until import log


class Model():
    """
    基类, 用来显示类的信息
    """
    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n {}>'.format(name, '\n '.join(properties))
        return s


def init():
    """
    初始化
    """
    driver = webdriver.Chrome()
    driver.get("https://www.huya.com/")
    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.refresh()
    return driver


def browser_login(driver: webdriver):
    """
    进入登陆页面并完成登陆
    """

    driver.find_element_by_id(Order.index_login.value).click()
    driver.switch_to_frame(Order.frame.value)
    try:
        driver.find_element_by_css_selector(Order.username.value).send_keys(config.username)
        driver.find_element_by_css_selector(Order.password.value).send_keys(config.password)
        time.sleep(2)
        driver.find_element_by_css_selector(Order.login_button.value).click()

    except Exception as e:
        log(e)
        raise(ZeroDivisionError("登陆标签有变导致 selenium 定位出错，请修正"))


def send_comments(driver: webdriver, room_title: str, comments: str):
    """
    发送评论功能
    """
    try:
        # 等待页面加载完成
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, Order.send_button.value))
        )

        driver.implicitly_wait(5)
        if element:
            tag = driver.find_element_by_css_selector(Order.comment.value)
            tag.send_keys(comments)
            # 发送成功写入日志
            log('normal [在房间 {} 发送了: {}]'.format(room_title, comments))
            time.sleep(1)
            tag.send_keys(Keys.ENTER)
            driver.find_element_by_css_selector(Order.send_button.value).click()
            time.sleep(0.5)

    except Exception as e:
        log('error ', e)
        raise ZeroDivisionError("发送评论标签有变导致 selenium 定位出错，请修正")


def _into_room_handle(driver: webdriver, comm: str, current_num: int):
    driver.implicitly_wait(5)

    room = driver.find_element_by_css_selector(Order.room_title.value.format(current_num+1))
    title = room.text
    room.click()

    driver.switch_to.window(driver.window_handles[1])
    send_comments(driver, title, comm)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def handle_room_tag(driver: webdriver, comm: str):
    """
    进入每一个直播, 并插播广告
    写入日志
    """
    # 将所有标签统计出来
    driver.execute_script(Order.page_end.value)
    sum_room = driver.find_elements_by_class_name(Order.room_tag.value)
    print(sum_room)
    i = 0
    while i < len(sum_room):
        try:
            _into_room_handle(driver, comm, i)
        except ElementClickInterceptedException:
            move_down(driver)
            _into_room_handle(driver, comm, i)
        i += 1

    try:
        move_down(driver)
        tag = driver.find_element_by_css_selector(Order.page_down.value)
        if tag:
            time.sleep(1)
            tag.click()
            driver.implicitly_wait(5)
            handle_room_tag(driver, comm)

    except NoSuchElementException:
        print("finish")
        driver.close()
        return


@time_spend
def main():
    driver = init()
    # 登陆
    browser_login(driver)
    # 进入直播页面
    into_live(driver)
    # 依次进入房间并发送弹幕
    handle_room_tag(driver, config.content)


if __name__ == '__main__':
    main()
