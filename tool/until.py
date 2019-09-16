import time


def log(*args, **kwargs):
    """
    日志功能,暂存于 tool.txt
    """
    # time.time() 返回 unix time
    time_format = '%Y/%m/%d %H:%M:%S'
    localtime = time.localtime(int(time.time()))
    formatted = time.strftime(time_format, localtime)
    with open('log/run_log.txt', 'a', encoding='utf-8') as f:
        print(formatted, *args, **kwargs)
        print(formatted, *args, file=f, **kwargs)
