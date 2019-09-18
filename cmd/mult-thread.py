import queue
from selenium import webdriver
import threading
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from conf import config
from tool.comm_lib import _add_cookies, time_spend
from tool.enum_instance import Order


class conphantomjs:
    phantomjs_max = 1  # 同时开启phantomjs个数
    time_gap = 0.00001  # 开启phantomjs间隔
    timeout = 20  # 设置phantomjs超时时间
    service_args = ['--disk-cache=yes']  # 参数设置

    def __init__(self):
        self.q_phantomjs = queue.Queue()  # 存放phantomjs进程队列

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
            time.sleep(1)

            driver.implicitly_wait(5)
            if element:
                tag = driver.find_element_by_css_selector(Order.comment.value)
                tag.send_keys(config.content)
                # 发送成功写入日志
                # log('normal [在房间 {} 发送了: {}]'.format(room_title, config.content))
                time.sleep(1)
                # tag.send_keys(Keys.ENTER)
                driver.find_element_by_css_selector(Order.send_button.value).click()
                time.sleep(1)

        except Exception as e:
            # log('error ', e)
            print(ZeroDivisionError("发送评论标签有变导致 selenium 定位出错，请修正"))
            # TODO 发送失败后, 加入到新的队列再发送

        print(url)

        # PHANTOMJS可能存在一种BUG，多进程爬取时网页的信息会弄串了，访问空白页可以重置

        self.q_phantomjs.put(driver)

    def open_phantomjs(self):
        """
        多线程开启phantomjs进程
        """

        def open_threading():
            d = webdriver.Chrome(service_args=conphantomjs.service_args)
            d.implicitly_wait(conphantomjs.timeout)  # 设置超时时间
            d.set_page_load_timeout(conphantomjs.timeout)  # 设置超时时间

            self.q_phantomjs.put(d)  # 将phantomjs进程存入队列

        th = []
        for i in range(conphantomjs.phantomjs_max):
            t = threading.Thread(target=open_threading)
            th.append(t)
        for i in th:
            i.start()
            time.sleep(conphantomjs.time_gap)  # 设置开启的时间间隔
        for i in th:
            i.join()

    def close_phantomjs(self):
        """
        多线程关闭phantomjs对象
        """
        th = []

        def close_threading():
            d = self.q_phantomjs.get()
            d.quit()

        for i in range(self.q_phantomjs.qsize()):
            t = threading.Thread(target=close_threading)
            th.append(t)
        for i in th:
            i.start()
        for i in th:
            i.join()


@time_spend
def main():
    """
    用法：
    1.实例化类
    2.运行open_phantomjs 开启phantomjs进程
    3.运行handle_room函数，传入url
    4.运行close_phantomjs 关闭phantomjs进程
    """
    cur = conphantomjs()
    conphantomjs.phantomjs_max = 10
    cur.open_phantomjs()
    print("phantomjs num is ", cur.q_phantomjs.qsize())

    url_list = ['https://www.huya.com/uzi', 'https://www.huya.com/518512', 'https://www.huya.com/chuhe', 'https://www.huya.com/buqiuren', 'https://www.huya.com/1380', 'https://www.huya.com/990214', 'https://www.huya.com/hyq18000', 'https://www.huya.com/housangun', 'https://www.huya.com/417964', 'https://www.huya.com/yingying8808', 'https://www.huya.com/edc595', 'https://www.huya.com/saonan', 'https://www.huya.com/107222', 'https://www.huya.com/chaojie', 'https://www.huya.com/520529', 'https://www.huya.com/shangjin', 'https://www.huya.com/52700', 'https://www.huya.com/agbaozi', 'https://www.huya.com/chenzihao', 'https://www.huya.com/521715', 'https://www.huya.com/lpl', 'https://www.huya.com/408604', 'https://www.huya.com/552423', 'https://www.huya.com/kpl', 'https://www.huya.com/weiba0715', 'https://www.huya.com/hujiangjun', 'https://www.huya.com/baby25', 'https://www.huya.com/678398', 'https://www.huya.com/11342412', 'https://www.huya.com/951058', 'https://www.huya.com/990128', 'https://www.huya.com/742611', 'https://www.huya.com/400298', 'https://www.huya.com/11352908', 'https://www.huya.com/111288', 'https://www.huya.com/guanzongo', 'https://www.huya.com/daomeili', 'https://www.huya.com/yuanwang', 'https://www.huya.com/11342421', 'https://www.huya.com/587520', 'https://www.huya.com/100953', 'https://www.huya.com/sy233', 'https://www.huya.com/52503', 'https://www.huya.com/huyalijun', 'https://www.huya.com/lolee', 'https://www.huya.com/qingwa666', 'https://www.huya.com/668668', 'https://www.huya.com/475974', 'https://www.huya.com/501781', 'https://www.huya.com/517518', 'https://www.huya.com/991222', 'https://www.huya.com/11602045', 'https://www.huya.com/chenxi6', 'https://www.huya.com/414818', 'https://www.huya.com/592818', 'https://www.huya.com/miss', 'https://www.huya.com/494680', 'https://www.huya.com/11342386', 'https://www.huya.com/haoren', 'https://www.huya.com/364112', 'https://www.huya.com/990919', 'https://www.huya.com/520731', 'https://www.huya.com/5801xiaowei', 'https://www.huya.com/966988', 'https://www.huya.com/766518', 'https://www.huya.com/chushouguai', 'https://www.huya.com/11352970', 'https://www.huya.com/pcl', 'https://www.huya.com/18983187', 'https://www.huya.com/880201', 'https://www.huya.com/712722', 'https://www.huya.com/11601968', 'https://www.huya.com/676324', 'https://www.huya.com/102491', 'https://www.huya.com/17635616', 'https://www.huya.com/11352944', 'https://www.huya.com/981585', 'https://www.huya.com/520320', 'https://www.huya.com/970711', 'https://www.huya.com/nikichew', 'https://www.huya.com/592655', 'https://www.huya.com/lck', 'https://www.huya.com/sunshen', 'https://www.huya.com/761792', 'https://www.huya.com/527686', 'https://www.huya.com/hunterxw', 'https://www.huya.com/shiziwang', 'https://www.huya.com/213062', 'https://www.huya.com/10036887', 'https://www.huya.com/237501', 'https://www.huya.com/11352915', 'https://www.huya.com/915056', 'https://www.huya.com/clkimmy', 'https://www.huya.com/278933', 'https://www.huya.com/539497', 'https://www.huya.com/880215', 'https://www.huya.com/19392815', 'https://www.huya.com/13865165', 'https://www.huya.com/826178', 'https://www.huya.com/11947428', 'https://www.huya.com/cxldb', 'https://www.huya.com/godlie', 'https://www.huya.com/17821340', 'https://www.huya.com/15191606', 'https://www.huya.com/991202', 'https://www.huya.com/16533391', 'https://www.huya.com/18553978', 'https://www.huya.com/660005', 'https://www.huya.com/15364443', 'https://www.huya.com/990424', 'https://www.huya.com/11336726', 'https://www.huya.com/787164', 'https://www.huya.com/13056628', 'https://www.huya.com/baobaos', 'https://www.huya.com/ximen', 'https://www.huya.com/16502373', 'https://www.huya.com/19130213', 'https://www.huya.com/wanqiuswzhibo', 'https://www.huya.com/393427', 'https://www.huya.com/luolijiang']

    th = []
    for i in url_list:
        t = threading.Thread(target=cur.room_handle, args=(i,))
        th.append(t)
    for i in th:
        i.start()
    for i in th:
        i.join()
    cur.close_phantomjs()
    print("phantomjs num is ", cur.q_phantomjs.qsize())


if __name__ == "__main__":
    main()
