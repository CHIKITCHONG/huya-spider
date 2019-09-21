import queue
import multiprocessing as mp
import threading as td
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from cache.huya_cache import redis_cli_gen
from conf import config
from conf.config import server_addr, port
from tool.comm_lib import _add_cookies, time_spend
from tool.enum_instance import Order
from multiprocessing.managers import BaseManager

q = queue.Queue()


class QueueManager(BaseManager):
    pass


def working():
    QueueManager.register('get_task_queue')
    QueueManager.register('get_result_queue')
    m = QueueManager(address=(server_addr, port), authkey=b'wykj2019')
    m.connect()
    task = m.get_task_queue()
    return task


# 从task队列取任务,并把结果写入result队列:
def get_url_from_task():
    task = working()
    while True:
        try:
            sum = []
            result = task.get(timeout=1)
            print('获取到 {} 的信息,开始进入工作函数'.format(len(result)))
            page = len(result) // 2
            sum.append(result[:page])
            sum.append(result[page:])
            multiprocess_main(sum)
            time.sleep(5)

        except queue.Empty:
            print('队列为空,此次发送任务完成')
            break


class ThreadTaskViaChrome(object):
    chrome_max = 1  # 同时开启 chrome 个数
    time_gap = 0.00001  # 开启 chrome 间隔
    timeout = 30  # 设置 chrome 超时时间

    def __init__(self):
        self.q_phantomjs = q  # 存放phantomjs进程队列

    def room_handle(self, url: str):
        """
        一个主处理函数处理进入房间发评论
        """
        driver = self.q_phantomjs.get()
        driver.get(url)
        _add_cookies(driver)

        try:
            # 等待页面加载完成
            element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, Order.send_button.value))
            )
            # time.sleep(1)

            # driver.implicitly_wait(5)
            if element:
                tag = driver.find_element_by_css_selector(Order.comment.value)
                tag.send_keys(config.content)
                time.sleep(1)
                # 若要发送不止一条,请取消注释下行
                # tag.send_keys(Keys.ENTER)
                driver.find_element_by_css_selector(Order.send_button.value).click()
                # time.sleep(1)
                print('发送成功', url)

        except Exception as e:
            print('发送失败:', url, e)

        # 发送成功写入日志
        # log(url, "发送了 「{}」".format(config.content))
        self.q_phantomjs.put(driver)

    def open_chrome(self):
        """
        多线程开启 chrome 进程
        """
        def open_threading():
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            d = webdriver.Chrome(chrome_options=chrome_options)

            d.implicitly_wait(ThreadTaskViaChrome.timeout)  # 设置超时时间
            d.set_page_load_timeout(ThreadTaskViaChrome.timeout)  # 设置超时时间
            d.maximize_window()
            self.q_phantomjs.put(d)  # 将phantomjs进程存入队列

        task = []
        for i in range(ThreadTaskViaChrome.chrome_max):
            t = td.Thread(target=open_threading)
            task.append(t)
        for i in task:
            i.start()
            time.sleep(ThreadTaskViaChrome.time_gap)  # 设置开启的时间间隔
        for i in task:
            i.join()

    def close_chrome(self):
        """
        多线程关闭 chrome 对象
        """
        th = []

        def close_threading():
            d = self.q_phantomjs.get()
            d.quit()

        for i in range(self.q_phantomjs.qsize()):
            t = td.Thread(target=close_threading)
            th.append(t)
        for i in th:
            i.start()
        for i in th:
            i.join()


def thread_main(url_list):
    """
    用法：
    1.实例化类
    2.运行 open_chrome 开启 chrome 进程
    3.运行 handle_room 函数，传入url
    4.运行 close_chrome 关闭 chrome 进程
    """
    cur = ThreadTaskViaChrome()
    ThreadTaskViaChrome.chrome_max = 5
    cur.open_chrome()
    print("队列大小是 ", cur.q_phantomjs.qsize())

    # 批量取 url
    task = []
    for i in url_list:
        t = td.Thread(target=cur.room_handle, args=(i,))
        task.append(t)
    for i in task:
        i.start()
    for i in task:
        i.join()

    # 完成后把线程关掉
    cur.close_chrome()


def multiprocess_main(url_list):
    pool = mp.Pool(processes=2)
    for i in url_list:
        # 2个进程并行
        pool.apply_async(func=thread_main, args=(i,))

    pool.close()
    pool.join()


@time_spend
def main():
    get_url_from_task()


if __name__ == "__main__":
    main()
