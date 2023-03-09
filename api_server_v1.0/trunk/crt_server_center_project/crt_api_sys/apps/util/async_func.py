import os
import xlrd
import json
import uuid
import hashlib
import zipfile
import datetime

from hashlib import md5
from attrdict import AttrDict

default_origin = 'redis'

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


async def delete_cache(redis, table_name, record_id=None):
    """
    删除缓存
    :param redis: redis对象
    :param table_name:
    :param record_id:
    :return:
    """
    try:
        record_key = f"{table_name}-record*{record_id or ''}"
        records_key = f"{table_name}-records*"

        record_keys = await redis.keys(record_key)
        records_keys = await redis.keys(records_key)

        del_keys = [] + [r.decode() for r in record_keys] + [r.decode() for r in records_keys]
        del_keys = list(set(del_keys))

        if del_keys:
            # 清除全部缓存键
            result = await redis.delete(*del_keys)
            return True, result

    except Exception as e:
        return False, e

    return True, 0


def md5_encryption(word, salt=None):
    word = f'{word}_{salt}' if salt else word
    md5_obj = md5()
    md5_obj.update(word.encode())
    return md5_obj.hexdigest()


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


def data_pag(records, page, per_page, to_json=True):
    """分页"""
    if isinstance(records, dict):
        records = list(records.values())

    result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

    result['record_size'] = len(records)

    divisor, remainder = divmod(len(records), per_page)
    result['page_size'] = (divisor + 1 if remainder > 0 else divisor) if page else 0

    records = records[(page - 1) * per_page:page * per_page] if page else records

    if to_json:
        result['items'] = [json.loads(record) for record in records]
    else:
        result['items'] = records

    return result


async def default_handle_sql(redis, table_name, op_type, record_id=None):
    """
        默认实现, 统一处理
        两条规则:
            1 根据 user_id, 清理 table_name 关联的记录
            2 根据 user_id, 清理 table_name 列表关联的记录
    :param redis:  redis对象
    :param table_name:  表名
    :param op_type:  数据库操作方式
    :param record_id:  记录id
    :return:
    """
    if op_type in ('insert', 'update', 'delete'):

        record_key = f'{table_name}-record:{record_id}'
        records_key = f'*{table_name}*-records:*'

        try:
            record_keys = redis.keys(record_key)
            records_keys = redis.keys(records_key)

            del_keys = [] + [r.decode() for r in record_keys] + [r.decode() for r in records_keys]

            if del_keys:
                # 清除全部缓存键
                result = redis.delete(*del_keys)
                return True, result

        except Exception as e:
            return False, e

    return True, 0


def read_excel(filename, del_excel=True):
    excel = xlrd.open_workbook(filename)
    # table = excel.sheet_by_name("工作表1")  # 根据名称获取sheet
    # table = excel.sheets()[0]  # 获取第一个sheet
    table = excel.sheet_by_index(0)  # 获取第一个sheet
    keys = table.row_values(1)  # 获取第一行所有内容，如果括号中1就是第二行，这点跟列表索引类似
    row_num = table.nrows - 1  # 获取工作表的有效行数，第一行为列名，略过
    col_num = table.ncols  # 获取工作表的有效列数

    table_data = []  # 定义一个空列表 存放所有表格数据
    for i in range(1, row_num):
        i += 1  # 第一行为标题，略过
        row_data = {}  # 定义一个空字典 存放行数据
        for j in range(col_num):
            c_type = table.cell(i, j).ctype  # 获取单元格数据类型
            c_cell = table.cell_value(i, j)  # 获取单元格数据
            if c_type == 2 and c_cell % 1 == 0:  # 如果是整形
                c_cell = int(c_cell)
            elif c_type == 3:  # 时间类型
                date = datetime.datetime(*xlrd.xldate_as_tuple(c_cell, 0))  # 转成datetime对象
                c_cell = date.strftime('%Y-%m-%d')
            elif c_type == 4:  # bool类型
                c_cell = True if c_cell == 1 else False

            # 循环每一个有效的单元格，将字段与值对应存储到字典中  字典的key就是excel表中每列第一行的字段
            row_data[keys[j]] = c_cell

        # 再将字典追加到列表中
        table_data.append(row_data)

    if del_excel and os.path.isfile(filename):
        os.remove(filename)

    return table_data


def read_many_sheets_excel(filename, del_excel=True):
    excel = xlrd.open_workbook(filename)
    all_table_data = {}

    for table in excel.sheets():
        keys = table.row_values(0)  # 获取第一行所有内容，如果括号中1就是第二行，这点跟列表索引类似
        row_num = table.nrows - 1  # 获取工作表的有效行数，第一行为列名，略过
        col_num = table.ncols  # 获取工作表的有效列数

        table_data = []  # 定义一个空列表 存放所有表格数据
        for i in range(0, row_num):
            i += 1  # 第一行为标题，略过
            row_data = {}  # 定义一个空字典 存放行数据
            for j in range(col_num):
                c_type = table.cell(i, j).ctype  # 获取单元格数据类型
                c_cell = table.cell_value(i, j)  # 获取单元格数据
                if c_type == 2 and c_cell % 1 == 0:  # 如果是整形
                    c_cell = int(c_cell)
                elif c_type == 3:  # 时间类型
                    date = datetime.datetime(*xlrd.xldate_as_tuple(c_cell, 0))  # 转成datetime对象
                    c_cell = date.strftime('%Y-%m-%d')
                elif c_type == 4:  # bool类型
                    c_cell = True if c_cell == 1 else False

                # 循环每一个有效的单元格，将字段与值对应存储到字典中  字典的key就是excel表中每列第一行的字段
                row_data[keys[j]] = c_cell

            # 再将字典追加到列表中
            table_data.append(row_data)

        all_table_data[table.name] = table_data

    if del_excel and os.path.isfile(filename):
        os.remove(filename)

    return all_table_data


def parse_mysql_url(mysql_url):
    mysql_url = mysql_url[17:]
    mysql_url = mysql_url.split(':')
    info_1 = mysql_url[1].split('@')
    info_2 = mysql_url[2].split('/')
    mysql_user = mysql_url[0]
    mysql_password = info_1[0]
    mysql_host = info_1[1]
    mysql_port = info_2[0]
    mysql_db = info_2[1]
    return mysql_user, mysql_password, mysql_host, mysql_port, mysql_db


async def backups_sql(mysql_url, backups_path):
    """备份sql文件到指定目录"""
    mysql_user, mysql_password, mysql_host, mysql_port, mysql_db = parse_mysql_url(mysql_url)

    # os.system(f"mysqldump -uroot -p123456 -h 127.0.0.1 -P 13306 --column-statistics=0 -d crt_test > {path}/backups/create_table_backup.sql")  # 备份表结构
    # os.system(f"mysqldump -uroot -p123456 -h 127.0.0.1 -P 13306 --column-statistics=0 -t crt_test > {path}/backups/table_data_backup.sql")  # 备份表数据
    # os.system(f"mysqldump -uroot -p123456 -h 127.0.0.1 -P 13306 -d crt_test > {backups_path}/create_table_backup.sql")  # 备份表结构
    # os.system(f"mysqldump -uroot -p123456 -h 127.0.0.1 -P 13306 -t crt_test > {backups_path}/table_data_backup.sql")  # 备份表数据
    os.system(f"mysqldump -u{mysql_user} -p{mysql_password} -h {mysql_host} -P {mysql_port} -d {mysql_db} > {backups_path}/create_table_backup.sql")  # 备份表结构
    os.system(f"mysqldump -u{mysql_user} -p{mysql_password} -h {mysql_host} -P {mysql_port} -t {mysql_db} > {backups_path}/table_data_backup.sql")  # 备份表数据


async def zip_dir(dir_path, zip_path=None):
    """压缩文件夹"""

    if not zip_path:
        zip_path = f'{dir_path}.zip'

    _zip = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)  # zip对象
    for dir_path, dir_names, filenames in os.walk(dir_path):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        f_path = dir_path.replace(dir_path, '')

        for filename in filenames:
            _zip.write(os.path.join(dir_path, filename), os.path.join(f_path, filename))
    _zip.close()


