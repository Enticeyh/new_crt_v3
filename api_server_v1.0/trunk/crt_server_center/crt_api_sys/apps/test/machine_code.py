import uuid
import time

array = [
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
    "w", "x", "y", "z",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
    "W", "X", "Y", "Z"
]


def get_short_id():
    id = str(uuid.uuid4()).replace("-", '')  # 注意这里需要用uuid4
    buffer = []
    for i in range(0, 8):
        start = i * 4
        end = i * 4 + 4
        val = int(id[start:end], 16)
        buffer.append(array[val % 62])
    return "".join(buffer)


if __name__ == '__main__':
    print(get_short_id())
    # start = time.time()
    # id_set = set()  # 用于存放生成的唯一id
    # count = 0  # 用于统计出现重复的次数
    # index = []  # 记录第几次调用生成8位id出现重复
    # for i in range(0, 20000000):
    #     id = get_short_id()
    #     if id in id_set:
    #         count += 1
    #         index.append(str(i + 1))
    #     else:
    #         id_set.add(id)
    #     # print('id：%s, 运行第 %s 次, 重复数:%s , 重复率:%s, 出现重复次序 %s' % (id, i + 1, count, count / (i + 1) * 100, ','.join(index)))
    # print(count, index)  # 1 ['17305371']  1 ['18980372']
    # print(time.time() - start)  # 189.43312883377075
