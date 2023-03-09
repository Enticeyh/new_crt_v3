import hashlib


def hash_func_params(*args, **kwargs):
    """
        格式化位置参数和关键字参数
            eg.
                a|b|c|?k=v&k=v
    """

    args_list = [str(_it) for _it in args]
    args_list.sort()

    kwargs_keys_list = list(kwargs.keys())
    kwargs_keys_list.sort()
    kwargs_list = [f'{_it}={kwargs[_it]}' for _it in kwargs_keys_list]

    params_msg = f'{"|".join(args_list)}?{"&".join(kwargs_list)}'
    md5_obj = hashlib.md5(params_msg.encode())
    return md5_obj.hexdigest()


def test(name, start, end):
    if not name and not all([start, end]):
        print('11111111111111')
    if all([start, end]) and (start <= 0 or end <= 0):
        print('222222222222222222222')
    if all([start, end]) and start > end:
        print('333333333333333333')


if __name__ == '__main__':
    test(None, -1, -2)
    print(hash_func_params(page=0, per_page=10, floor_id=1))
