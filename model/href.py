import time
from typing import List

from model import Model


class Href(Model):
    """
    Session 是用来保存 session 的 model
    """

    def __init__(self, lst: List[str]):
        super().__init__(lst)


if __name__ == '__main__':

    lst = ['https://www.huya.com/uzi', 'https://www.huya.com/lafeng', 'https://www.huya.com/52700',
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

    m = Href(lst)
    m.save()
