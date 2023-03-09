import io
import os

from PIL import Image
from os.path import dirname, realpath
from base64 import b64encode

def test1():
    # 读取svg图片文件
    root_project_dir = dirname(dirname(realpath(__file__)))
    print(root_project_dir)
    svg_path = f'{root_project_dir}/static/photo/1层.svg'
    with open(file=svg_path, mode='rb+') as f:
        # lines = f.readlines()
        # lines.pop()
        # print(type(lines))
        # print(lines[-1])
        f.seek(-6, os.SEEK_END)
        f.truncate()

        # 追加点位信息
        coordinate_X = 621
        coordinate_Y = 273
        rate = 0.0274223000
        angle = 90
        # icon_path = 'http://127.0.0.1:8000/static/icon_image/SmokeDetector.png'
        icon_path = f'{root_project_dir}/static/icon_image/double_lamp.png'

        img = Image.open(icon_path)

        if angle:
            img = img.rotate(angle)  # 旋转图片
            # img.save(f'{root_project_dir}/double_lamp_rotate.png')  # 保存图片

        width = img.width
        height = img.height
        if rate:
            width *= rate
            height *= rate

        # 创建data_uri
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        encoded_data = b64encode(img_byte_arr).decode("utf-8").strip()
        href = f'data:image/png;base64,{encoded_data}'
        print(href)

        info = f'<image width="{width}" height="{height}" x="{coordinate_X}" y="{coordinate_Y}" href="{href}"></image>\n'

        f.write(info.encode())
        f.write("</svg>".encode())

    # 保存成新的svg图片

    # 将文件路径保存


def test2():
    # 读取svg图片文件
    root_project_dir = dirname(dirname(realpath(__file__)))
    path = '/static/photo/1层.svg'
    with open(file=f'{root_project_dir}{path}', mode='r') as f:
        lines = f.readlines()

    # 保存成新的svg图片
    quick_svg_path = f'{path[:-4]}_quick_svg.svg'
    with open(file=f'{root_project_dir}{quick_svg_path}', mode='w') as f:
        lines.pop()

        # 追加点位信息
        coordinate_X = 257
        coordinate_Y = 332
        rate = 0.274223000
        angle = 90
        icon_path = f'{root_project_dir}/static/icon_image/double_lamp.png'

        img = Image.open(icon_path)

        if angle:
            img = img.rotate(angle)  # 旋转图片

        width = img.width
        height = img.height
        if rate:
            width *= rate
            height *= rate

        # 创建data_uri
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        encoded_data = b64encode(img_byte_arr).decode("utf-8").strip()
        href = f'data:image/png;base64,{encoded_data}'

        info = f'<image width="{width}" height="{height}" x="{coordinate_X}" y="{coordinate_Y}" href="{href}"></image>\n'

        lines.append(info)
        lines.append("</svg>")

        f.write(''.join(lines))

    # 将文件路径保存
    print(quick_svg_path)


if __name__ == '__main__':
    # test1()
    test2()
