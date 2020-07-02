#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    obfuscate.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    遍历工程目录，把目录里的*.py文件写入cython的编译配置文件
    
    :author: leo
    :copyright: (c) 2020, Tungee
    :date created: 2020-04-27 11:14
 
"""
import os
import shutil

import click

APP_NAME = 'bubble'

SETUP_FILE = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import Cython.Compiler
import os


def py_to_so():
    try:
        ext_modules = [
            {}
        ]
        setup(
            name="py to so",
            ext_modules=cythonize(ext_modules, language_level=2),
        )
    except Cython.Compiler.Errors.CompileError as e:
        # 捕获异常，从报错信息的最后一行获取文件名并格式化
        filename = str(e).split('\\n')[-1]
        os.popen(
            'autopep8 --in-place --aggressive --aggressive ' +
            os.getcwd() +
            "/" +
            filename)
        # 继续转换
        py_to_so()


py_to_so()

"""

# FIXME: 指定编译的文件，不指定就默认生成所有文件
build_files = [
    'apps/config.py',
    'apps/auth/helpers.py',
    'apps/auth/views.py',
    'apps/models/mongo/user.py',
    'apps/api/views.py',
    'apps/api/resources/user.py',
]


@click.command()
@click.option('--src_dir', default='{}'.format(APP_NAME), help='源文件夹')
@click.option('--dst_dir', default='deploy/{}'.format(APP_NAME), help='混淆后的文件夹，注意这个目录会默认先清除')
@click.option('--include_init', default=False, help='是否包含__init__.py文件')
def main(src_dir, dst_dir, include_init):
    # 复制源码到指定目录
    # TODO：这样暴力切割如果用户传入的路径包含了app的名字会有问题
    target_dir_name = dst_dir.split(APP_NAME, 1)[0]
    shutil.rmtree(os.path.join(os.path.dirname(os.path.abspath(__file__)), dst_dir), ignore_errors=True)
    os.makedirs(target_dir_name, exist_ok=True)
    os.system("cp -R {} {}".format(os.path.join(os.path.dirname(os.path.abspath(__file__)), src_dir), dst_dir))

    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), target_dir_name))
    ext_list = []
    if build_files:
        # 指定了编译的文件
        for bf in build_files:
            df = bf.replace('.py', '').replace('/', '.')
            ext_list.append("Extension('{}', ['{}'])".format(df, bf))
        with open('setup.py', 'w') as f:
            f.write(SETUP_FILE.format(',\n\t\t\t'.join(ext_list)))
    else:
        include_init = bool(include_init)
        tree = os.walk(APP_NAME)
        for path, _, file_list in tree:
            if include_init:
                for file_name in file_list:
                    _file_path = os.path.join(path, file_name)
                    _dot_path = _file_path.replace('.py', '').replace('/', '.')
                    if file_name.endswith('.py'):
                        build_files.append(_file_path)
                        ext_list.append("Extension('{}', ['{}'])".format(_dot_path, _file_path))
            else:
                for file_name in file_list:
                    _file_path = os.path.join(path, file_name)
                    _dot_path = _file_path.replace('.py', '').replace('/', '.')
                    if file_name.endswith('.py') and file_name != '__init__.py':
                        build_files.append(_file_path)
                        ext_list.append("Extension('{}', ['{}'])".format(_dot_path, _file_path))
        with open('setup.py', 'w') as f:
            f.write(SETUP_FILE.format(',\n\t\t\t'.join(ext_list)))
    # 执行编译命令
    os.system("python setup.py build_ext --inplace")

    # 删除app里的已编译的.py和.c文件
    os.system("find %s -name \"*.pyc\" -type f -print -exec rm -rf {} \\;" % APP_NAME)
    os.system("find %s -name \"*.c\" -type f -print -exec rm -rf {} \\;" % APP_NAME)

    tree = os.walk(APP_NAME)
    for path, _, file_list in tree:
        for file_name in file_list:
            _file_path = os.path.join(path, file_name)
            if _file_path in build_files:
                print('清除经过编译的py文件: {}'.format(_file_path))
                os.remove(_file_path)

    # 剩余的py文件就编译成.pyc，然后移除剩余的.py文件
    os.system("python3 -m compileall -f -b %s" % APP_NAME)
    os.system("find %s -name \"*.py\" -type f -print -exec rm -rf {} \\;" % APP_NAME)


if __name__ == '__main__':
    main()
