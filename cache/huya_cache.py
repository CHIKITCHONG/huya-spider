import redis


def redis_cli_gen():
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_response=True)
    r = redis.Redis(connection_pool=pool)
    s = r.pubsub()
    s.ps.subscribe('huya-spider')  # 从 huya-spider 订阅消息
    return s
