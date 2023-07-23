# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : run.py
# ------------------------------------------------------------------------------
#
# File          : run.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import os, sys, subprocess
import shutil
from _dev.help_generator.define import DOC_PATH,DOC_DEV_PATH
from mbt.resources import HELP_PATH

# create a new project use command line:
# ->python path\scripts\sphinx-quickstart -q -p "mbt" -a "Zhang, Haag" -v "1.0"
# the command for building a hpp file see below.
# ->set SPHINXBUILD="path-to-python\Scripts\sphinx-build"
# ->call path-to-make.bat\make.bat htmlhelp

def task_build_mbt_help_html(timeout=10):
    _path = os.path.join(os.path.dirname(sys.executable), 'Scripts', 'sphinx-build')
    _make_bat = os.path.join(DOC_PATH, 'make.bat')
    _build_path=os.path.join(DOC_PATH,'_build','htmlhelp')
    _dst_path=os.path.join(HELP_PATH,'book_mbthelp')
    _cmds = ['set SPHINXBUILD={}'.format(_path),
             'call {} htmlhelp'.format(_make_bat)]
    _p = subprocess.Popen('cmd.exe', shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    for cmd in _cmds:
        _p.stdin.write((cmd + "\n").encode('utf-8'))
    _p.stdin.close()
    _p.wait(timeout)
    if not os.path.exists(_dst_path):
        os.makedirs(_dst_path)
    print('copy file to path %s'%_dst_path)
    shutil.copytree(_build_path, _dst_path,dirs_exist_ok=True)

    return _p.returncode, _p.stdout.read().decode('utf-8')

def task_build_mbt_dev_help_html(timeout=10):
    _path = os.path.join(os.path.dirname(sys.executable), 'Scripts', 'sphinx-build')
    _make_bat = os.path.join(DOC_DEV_PATH, 'make.bat')
    _build_path=os.path.join(DOC_DEV_PATH,'_build','htmlhelp')
    _dst_path=os.path.join(HELP_PATH,'book_mbtdevhelp')
    _cmds = ['set SPHINXBUILD={}'.format(_path),
             'call {} htmlhelp'.format(_make_bat)]
    _p = subprocess.Popen('cmd.exe', shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    for cmd in _cmds:
        _p.stdin.write((cmd + "\n").encode('utf-8'))
    _p.stdin.close()
    _p.wait(timeout)
    if not os.path.exists(_dst_path):
        os.makedirs(_dst_path)
    print('copy file to path %s'%_dst_path)
    shutil.copytree(_build_path, _dst_path,dirs_exist_ok=True)

    return _p.returncode, _p.stdout.read().decode('utf-8')