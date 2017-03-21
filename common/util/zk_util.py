import json

from kazoo.client import KazooClient

from common.settings import CACHE_TIMEOUT, REDIS_HOST, REDIS_PORT
from common.util.redis_util import r_get_str, r_set_str_with_timeout

zk = KazooClient(
    hosts='{host}:{port}'.format(host=REDIS_HOST, port=REDIS_PORT),
    read_only=True
)


def _zk_cache_get(path):
    return r_get_str(path)


def _zk_cache_set(path, data):
    return r_set_str_with_timeout(path, data, CACHE_TIMEOUT)


def _get_path_from_zk(path):
    zk.start()
    if zk.exists(path):
        data, stat = zk.get(path)
    zk.stop()
    _zk_cache_set(path, data)
    return data


def zk_get_dict(path):
    res = _zk_cache_get(path)
    if res is None:
        res = _get_path_from_zk(path)
    return json.loads(res)
