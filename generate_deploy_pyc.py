#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    obfuscate.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    遍历工程目录，并对目录里的*.py文件进行混淆
    
    :author: leo
    :copyright: (c) 2020, Tungee
    :date created: 2020-04-27 11:14
 
"""
import os
import shutil

import click

APP_NAME = 'bubble'


@click.command()
@click.option('--src_dir', default='./{}'.format(APP_NAME), help='源文件夹')
@click.option('--dst_dir', default='./deploy/{}'.format(APP_NAME), help='混淆后的文件夹，注意这个目录会默认先清除')
def main(src_dir, dst_dir):
    # 在目标目录构建源目录结构
    shutil.rmtree(dst_dir, ignore_errors=True)
    tree = os.walk(src_dir)
    for path, dir_list, _ in tree:
        for dir_name in dir_list:
            _dst_dir = os.path.join(path.replace(src_dir, dst_dir, 1), dir_name)
            os.makedirs(_dst_dir, exist_ok=True)
    # 混淆文件并保存
    tree = os.walk(src_dir)
    for path, _, file_list in tree:
        for file_name in file_list:
            _src_file_path = os.path.join(path, file_name)
            _dst_file_path = os.path.join(path.replace(src_dir, dst_dir, 1), file_name)
            shutil.copy(_src_file_path, _dst_file_path)
            print('复制文件：{}...'.format(_src_file_path))
            # TODO: 如何混淆加密整个工程
            # if not file_name.endswith('.py'):
            #     # 直接复制源文件
            #     shutil.copy(_src_file_path, _dst_file_path)
            #     print('复制文件：{}...'.format(_src_file_path))
            #     continue
            # print('混淆文件：{}...'.format(_src_file_path))
            # _obfuscate_exec = 'pyminifier --obfuscate -o {dst} {src}'.format(dst=_dst_file_path, src=_src_file_path)
            # os.system(_obfuscate_exec)

    # 编译成.pyc，删除原有的.py
    os.system("python3 -m compileall -f -b %s" % dst_dir)
    os.system("find %s -name \"*.py\" -type f -print -exec rm -rf {} \\;" % dst_dir)


if __name__ == '__main__':
    main()
