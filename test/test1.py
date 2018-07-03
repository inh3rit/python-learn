import threading

data = {}


def fun_timer():
    print('test')
    global timer
    timer = threading.Timer(600, fun_timer)
    timer.start()


if __name__ == "__main__":
    timer = threading.Timer(0, fun_timer)
    timer.start()


def get_users():
    return ['a', 'b', 'c', 'd', 'e']


