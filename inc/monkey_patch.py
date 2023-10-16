import requests
import time
import threading
import functools
from inc import common

def sleep_interval(f):
    lock = threading.Lock()
    last_time = 0

    @functools.wraps(f)
    def _wrap(*args, **kwargs):
        nonlocal last_time
        with lock:
            duration = time.perf_counter() - last_time
            if duration < common.get_value("request_interval"):
                time.sleep(common.get_value("request_interval") - duration)
            last_time = time.perf_counter()
        return f(*args, **kwargs)

    return _wrap



def auto_retry_429(f):
    @functools.wraps(f)
    def _wrap(*args, **kwargs):
        while True:
            resp = f(*args, **kwargs)
            if isinstance(resp, requests.Response) and resp.status_code == 429:
                continue
            return resp

    return _wrap


def auto_retry(retry_times):
    def wrapper(f):
        @functools.wraps(f)
        def _wrap(*args, **kwargs):
            for _ in range(retry_times - 1):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    print("Auto retry: " + repr(e))
                    pass
            return f(*args, **kwargs)

        return _wrap

    return wrapper


def monkey_patch_all():
    # 因为request.request最终调用request.Session.request, 我们只需要patch session的request函数
    requests.Session.request = sleep_interval(requests.Session.request)
    requests.Session.request = auto_retry_429(requests.Session.request)
    requests.get = auto_retry(5)(requests.get)


if __name__ == "__main__":
    for _ in range(5):
        print(requests.get("http://baidu.com").status_code)
