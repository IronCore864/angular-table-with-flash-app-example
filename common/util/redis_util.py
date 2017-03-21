import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)


def r_get_str(key):
    return r.get(key)


def r_set_str(key, value):
    return r.set(key, value)


def r_set_str_with_timeout(key, value, timeout):
    return r.set(key, value, timeout)
