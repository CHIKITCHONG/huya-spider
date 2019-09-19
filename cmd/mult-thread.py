import queue
from selenium import webdriver
import threading
import time

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from conf import config
from tool.comm_lib import _add_cookies, time_spend
from tool.enum_instance import Order
from tool.until import log


lock = threading.Lock()

q = queue.Queue()


class ThreadTaskViaChrome(object):
    chrome_max = 1  # 同时开启 chrome 个数
    time_gap = 0.00001  # 开启 chrome 间隔
    timeout = 20  # 设置 chrome 超时时间

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
            time.sleep(1)

            driver.implicitly_wait(5)
            if element:
                tag = driver.find_element_by_css_selector(Order.comment.value)
                tag.send_keys(config.content)
                time.sleep(1)
                # 若要发送不止一条,请取消注释下行
                # tag.send_keys(Keys.ENTER)
                driver.find_element_by_css_selector(Order.send_button.value).click()
                time.sleep(1)

        except Exception as e:
            print(url, '\n', e)
            print(ZeroDivisionError("发送评论标签有变导致 selenium 定位出错，请修正"))
            # TODO 发送失败后, 加入到新的队列再发送

        # 发送成功写入日志
        # log(url, "发送了 「{}」".format(config.content))
        print(url)
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
            t = threading.Thread(target=open_threading)
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
    2.运行 open_chrome 开启 chrome 进程
    3.运行 handle_room 函数，传入url
    4.运行 close_chrome 关闭 chrome 进程
    """
    cur = ThreadTaskViaChrome()
    ThreadTaskViaChrome.chrome_max = 10
    cur.open_chrome()
    print("队列大小是 ", cur.q_phantomjs.qsize())

    # 批量取 url
    url_list = ['https://www.huya.com/102411', 'https://www.huya.com/pcl', 'https://www.huya.com/godv', 'https://www.huya.com/518512', 'https://www.huya.com/281710', 'https://www.huya.com/chuhe', 'https://www.huya.com/buqiuren', 'https://www.huya.com/518518', 'https://www.huya.com/hyq18000', 'https://www.huya.com/125393', 'https://www.huya.com/kpl', 'https://www.huya.com/shangjin', 'https://www.huya.com/229085', 'https://www.huya.com/edc595', 'https://www.huya.com/weiba0715', 'https://www.huya.com/saonan', 'https://www.huya.com/417964', 'https://www.huya.com/agbaozi', 'https://www.huya.com/11342412', 'https://www.huya.com/pp1204', 'https://www.huya.com/hujiangjun', 'https://www.huya.com/678398', 'https://www.huya.com/chenzihao', 'https://www.huya.com/11342421', 'https://www.huya.com/111288', 'https://www.huya.com/daomeili', 'https://www.huya.com/712722', 'https://www.huya.com/dasdad', 'https://www.huya.com/11352908', 'https://www.huya.com/520214', 'https://www.huya.com/housangun', 'https://www.huya.com/lpl', 'https://www.huya.com/475974', 'https://www.huya.com/501781', 'https://www.huya.com/yingying8808', 'https://www.huya.com/gushouyu', 'https://www.huya.com/400298', 'https://www.huya.com/742610', 'https://www.huya.com/11342390', 'https://www.huya.com/527686', 'https://www.huya.com/qingwa666', 'https://www.huya.com/nanyanx', 'https://www.huya.com/baby25', 'https://www.huya.com/19506901', 'https://www.huya.com/miguandidi', 'https://www.huya.com/guanzongo', 'https://www.huya.com/yuanwang', 'https://www.huya.com/dongji', 'https://www.huya.com/391226', 'https://www.huya.com/539497', 'https://www.huya.com/wangshi520', 'https://www.huya.com/aluka', 'https://www.huya.com/278933', 'https://www.huya.com/520852', 'https://www.huya.com/520524', 'https://www.huya.com/818929', 'https://www.huya.com/522222', 'https://www.huya.com/520187', 'https://www.huya.com/11352914', 'https://www.huya.com/14982948', 'https://www.huya.com/chenxi6', 'https://www.huya.com/gucun', 'https://www.huya.com/11352970', 'https://www.huya.com/miss', 'https://www.huya.com/18635783', 'https://www.huya.com/sambty', 'https://www.huya.com/483547', 'https://www.huya.com/227351', 'https://www.huya.com/chushouguai', 'https://www.huya.com/mhqiezi', 'https://www.huya.com/520320', 'https://www.huya.com/11342386', 'https://www.huya.com/5801xiaowei', 'https://www.huya.com/ximen', 'https://www.huya.com/17635616', 'https://www.huya.com/11342414', 'https://www.huya.com/clkimmy', 'https://www.huya.com/102491', 'https://www.huya.com/lck', 'https://www.huya.com/10193973', 'https://www.huya.com/11342396', 'https://www.huya.com/miqijieshuo', 'https://www.huya.com/11718650', 'https://www.huya.com/981585', 'https://www.huya.com/19225444', 'https://www.huya.com/11352915', 'https://www.huya.com/qiguaijun', 'https://www.huya.com/haoren', 'https://www.huya.com/641641', 'https://www.huya.com/521715', 'https://www.huya.com/637829', 'https://www.huya.com/mifengaaa', 'https://www.huya.com/769178', 'https://www.huya.com/59252', 'https://www.huya.com/luolijiang', 'https://www.huya.com/11352944', 'https://www.huya.com/13865165', 'https://www.huya.com/sunshen', 'https://www.huya.com/15483489', 'https://www.huya.com/shiziwang', 'https://www.huya.com/880215', 'https://www.huya.com/guihu', 'https://www.huya.com/688062', 'https://www.huya.com/18390080', 'https://www.huya.com/11947428', 'https://www.huya.com/adgll', 'https://www.huya.com/213062', 'https://www.huya.com/930671', 'https://www.huya.com/592818', 'https://www.huya.com/513533', 'https://www.huya.com/564721', 'https://www.huya.com/970711', 'https://www.huya.com/761792', 'https://www.huya.com/757206', 'https://www.huya.com/shiyue', 'https://www.huya.com/592655', 'https://www.huya.com/sy233', 'https://www.huya.com/godlie', 'https://www.huya.com/wutaiyang', 'https://www.huya.com/19191461']

    task = []
    for i in url_list:
        t = threading.Thread(target=cur.room_handle, args=(i,))
        task.append(t)
    for i in task:
        i.start()
    for i in task:
        i.join()

    cur.close_chrome()
    print("运行结束", "\n", "关闭线程后还有{}个线程".format(cur.q_phantomjs.qsize()))


if __name__ == "__main__":
    main()
