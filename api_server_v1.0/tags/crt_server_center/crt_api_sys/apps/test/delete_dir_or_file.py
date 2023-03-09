# 遍历并删除指定名称的文件夹及其中的文件
# /mnt/d/MyProject/new_crt_v1.0/api_server_v1.0/trunk/crt_server_center/crt_api_sys/apps/test/delete_dir_or_file.py
import os
import shutil

path = "/mnt/d/Desktop/crt_server_center/aliyun/crt_server_center"
# path = os.path.abspath(".")

# print(__file__)  # 获取当前py文件路径
# print(os.path.abspath("."))  # 获取调用py文件时的命令路径

# walk函数的第一个参数path用于指定要遍历内容的根目录
for root, dirs, files in os.walk(path):
    '''
    walk()函数返回一个包括3个元素(dir_path, dir_names,file_names)的元组生成器对象。其中dir_path表示当前遍历的
    路径，是一个字符串；dir_names表示当前路径下包含的子目录，是一个列表；file_names表示当前路径下包含的文件
    ，也是一个列表。
    '''

    if root.endswith("__pycache__"):
        # os.rmdir(root)  # 如果要删除的目录非空（其下还包含有文件或文件夹），则不能删除
        shutil.rmtree(root)  # 删除目录及目录下的文件和子目录
