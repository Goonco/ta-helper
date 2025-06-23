import os
import time
from functools import wraps
import shutil

def clean_up(paths) :
    for path in paths :
        safe_remove(path)

def safe_remove(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def check_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time

        print(f"[{func.__name__}] : {duration:.4f}s")

        return result

    return wrapper
