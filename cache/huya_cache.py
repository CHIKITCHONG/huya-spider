import redis


def redis_cli_gen():
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_response=True)
    r = redis.Redis(connection_pool=pool)
    return r
