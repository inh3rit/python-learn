a = {0: 1, 1: 2, 2: 5}
b = {}

def func():
    global a
    for i in range(4):
        if (a.keys().__contains__(i)):
            b[i] = a[i]
        else:
            b[i] = 0
        print(b)
        a = b

func()
print(a)
