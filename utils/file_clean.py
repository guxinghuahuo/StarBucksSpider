import os
import re

def clean_filename(name):
    # 定义非法字符集（Windows 不允许这些字符作为文件名）
    illeagal_chars = r'\/:*?"<>|'
    # 替换非法字符
    name = re.sub(r'[\\/:*?"<>|]', '_', name)
    # 移除其他不适合的字符（比如括号）
    name = re.sub(r'[（）]', '_', name)
    # 保证文件名不超过 255 个字符
    name = name[:255]
    return name