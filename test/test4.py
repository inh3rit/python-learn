import random

data = {'HTML': 32, 'CSS': 3, '图片': 2, '语音': 1, '视频': 1, 'FLASH': 1}


# for _ in range(20):
#     for k, v in data.items():
#         print(k, v)
#     print('----------------------------')
#
# for _ in range(20):
#     lst = range(10)
#     print(random.choice(lst))

def random_by_weight(dct):
    lst = []
    for k, v in dct.items():
        lst += [k] * v
    return random.choice(lst)


dct = {}
for _ in range(10000):
    k = random_by_weight(data)
    if dct.keys().__contains__(k):
        dct[k] += 1
    else:
        dct[k] = 1


print(dct)
