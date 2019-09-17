from enum import Enum


class Order(Enum):
    """
    枚举
    对应定位
    """
    # 首页登陆按钮
    index_login = "nav-login"
    # 登陆框架
    frame = "UDBSdkLgn_iframe"
    # 账户
    username = "#account-login-form > div:nth-child(1) > input"
    # 密码
    password = "#account-login-form > div:nth-child(2) > input"
    # 确认登录按钮
    login_button = "#account-login-form > div:nth-child(7)"
    # 评论框
    comment = "#pub_msg_input"
    # 评论发送按钮
    send_button = "#msg_send_bt"
    # 所有房间标签
    room_tag = "game-live-item"
    # 房间名称
    room_title = "#js-live-list > li:nth-child({}) > a.title.new-clickstat"
    # 房间链接
    room_href = "#js-live-list > li:nth-child({}) > a.title.new-clickstat:link"
    # 翻页
    page_down = "a[class=\"laypage_next\"]"
    # 滑至底部
    page_end = "var q=document.documentElement.scrollTop=100000"


if __name__ == '__main__':
    print(Order.username.value, type(Order.username))

