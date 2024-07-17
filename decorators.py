from time import time


def timer(foo):
    def wrapper(*args, **kwargs):
        start = time()
        result = foo(*args, **kwargs)
        finish = time()
        print(f'Time: {finish - start}')
    return wrapper
