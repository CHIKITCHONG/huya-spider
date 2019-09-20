import queue
import multiprocessing as mp
import threading as td
import time
import logging
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from cache.huya_cache import redis_cli_gen
from conf import config
from tool.comm_lib import _add_cookies, time_spend
from tool.enum_instance import Order


q = queue.Queue()


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


def multiprocess_main():
    # 开多进程
    url_list = [
        ['https://www.huya.com/uzi', 'https://www.huya.com/lafeng', 'https://www.huya.com/52700',
         'https://www.huya.com/417964', 'https://www.huya.com/1380', 'https://www.huya.com/loldongyueyue',
         'https://www.huya.com/12123', 'https://www.huya.com/408604', 'https://www.huya.com/haddis',
         'https://www.huya.com/maxiaoshuai', 'https://www.huya.com/518518', 'https://www.huya.com/agbaozi',
         'https://www.huya.com/107222', 'https://www.huya.com/11342412', 'https://www.huya.com/pp1204',
         'https://www.huya.com/housangun', 'https://www.huya.com/chenzihao', 'https://www.huya.com/991222',
         'https://www.huya.com/501781', 'https://www.huya.com/159409', 'https://www.huya.com/791166',
         'https://www.huya.com/bg90010abl', 'https://www.huya.com/776075', 'https://www.huya.com/11352908',
         'https://www.huya.com/378173', 'https://www.huya.com/shangjin', 'https://www.huya.com/616702',
         'https://www.huya.com/966988', 'https://www.huya.com/11342421', 'https://www.huya.com/125393',
         'https://www.huya.com/hujiangjun', 'https://www.huya.com/52503', 'https://www.huya.com/huyabuyi',
         'https://www.huya.com/19584140', 'https://www.huya.com/92601', 'https://www.huya.com/100953',
         'https://www.huya.com/gucun', 'https://www.huya.com/kpl', 'https://www.huya.com/11342414',
         'https://www.huya.com/13754079', 'https://www.huya.com/912597', 'https://www.huya.com/gushouyu',
         'https://www.huya.com/503376', 'https://www.huya.com/18682596', 'https://www.huya.com/447963',
         'https://www.huya.com/guanzongo', 'https://www.huya.com/19096820', 'https://www.huya.com/589193',
         'https://www.huya.com/11352915', 'https://www.huya.com/528017', 'https://www.huya.com/990919',
         'https://www.huya.com/yiwaa', 'https://www.huya.com/143075', 'https://www.huya.com/520731',
         'https://www.huya.com/17635616', 'https://www.huya.com/chushouguai', 'https://www.huya.com/huhuu',
         'https://www.huya.com/huyaoxiaoyu', 'https://www.huya.com/11352944', 'https://www.huya.com/816945']
        ,
        ['https://www.huya.com/lpl', 'https://www.huya.com/huaih', 'https://www.huya.com/feiduan1520',
         'https://www.huya.com/11352970', 'https://www.huya.com/18595696', 'https://www.huya.com/930671',
         'https://www.huya.com/qingwa666', 'https://www.huya.com/704593', 'https://www.huya.com/11342396',
         'https://www.huya.com/243680', 'https://www.huya.com/924898', 'https://www.huya.com/shangdi',
         'https://www.huya.com/11336726', 'https://www.huya.com/13865165', 'https://www.huya.com/sisi521',
         'https://www.huya.com/133880', 'https://www.huya.com/761792', 'https://www.huya.com/102491',
         'https://www.huya.com/978012', 'https://www.huya.com/cocoyue', 'https://www.huya.com/592655',
         'https://www.huya.com/5801xiaowei', 'https://www.huya.com/400298', 'https://www.huya.com/15107963',
         'https://www.huya.com/991202', 'https://www.huya.com/hunterxw', 'https://www.huya.com/10036887',
         'https://www.huya.com/19129736', 'https://www.huya.com/690482', 'https://www.huya.com/lck',
         'https://www.huya.com/221555', 'https://www.huya.com/660069', 'https://www.huya.com/kyjpcq',
         'https://www.huya.com/237501', 'https://www.huya.com/990424', 'https://www.huya.com/11342386',
         'https://www.huya.com/15598093', 'https://www.huya.com/miqijieshuo', 'https://www.huya.com/19675029',
         'https://www.huya.com/978013', 'https://www.huya.com/cxldb', 'https://www.huya.com/19377567',
         'https://www.huya.com/19392420', 'https://www.huya.com/16368110', 'https://www.huya.com/17611123',
         'https://www.huya.com/18012993', 'https://www.huya.com/213062', 'https://www.huya.com/19392815',
         'https://www.huya.com/880201', 'https://www.huya.com/978011', 'https://www.huya.com/adgll',
         'https://www.huya.com/981175', 'https://www.huya.com/915056', 'https://www.huya.com/272564',
         'https://www.huya.com/czj520wyy', 'https://www.huya.com/520635', 'https://www.huya.com/godlie',
         'https://www.huya.com/58dajin', 'https://www.huya.com/mianzai', 'https://www.huya.com/978016']
        ,
        ]

    pool = mp.Pool(processes=2)
    for i in url_list:
        # 2个进程并行
        pool.apply_async(func=thread_main, args=(i,))

    pool.close()
    pool.join()


# 订阅 redis 频道
def subscribe_from_redis(s) -> List[str]:
    resp = []
    msg = s.listen()

    # 监听状态：有消息发布了就拿过来
    for item in msg:
        if item['type'] == "message":
            data = str(item["data"], encoding="utf-8")
            resp.append(data)

    return resp


@time_spend
def worker(r):

    multiprocess_main()


def main():
    # 初始化 redis
    r = redis_cli_gen()

    # 调用 worker
    worker(r)


if __name__ == "__main__":
    main()
