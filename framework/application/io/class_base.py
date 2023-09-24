# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : Test Control System
# Sourcefile(s) : class_base.py
# ------------------------------------------------------------------------------
#
# File          : class_base.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import typing, os


class AppFileIO:

    def __init__(self, **kwargs):
        self.extension = kwargs.get('extension', '.txt')
        self.data = None
        self.filePath = kwargs.get('file_path')
        self.filename = kwargs.get('filename')
        self.error = ''

    def read(self, *args, **kwargs):
        pass

    def write(self, *args, **kwargs):
        pass

    def get_full_path(self):
        if '.' in self.filename:
            _file_name = self.filename
        else:
            _file_name = self.filename + self.extension
        return os.path.join(self.filePath, _file_name)

    def is_file_exist(self):
        _full_path = self.get_full_path()
        return os.path.exists(_full_path)

    def get_section(self, section_name: str):
        if self.data is not None and section_name in self.data:
            return self.data[section_name]

    @staticmethod
    def read_file_in_raw(path, flag='r', encoding='utf-8', in_lines=False) -> typing.AnyStr:
        with open(path, flag, encoding=encoding) as f:
            if in_lines:
                _ret = f.readlines()
            else:
                _ret = f.read()
        return _ret

    @staticmethod
    def write_file_in_raw(path, data, flag='w', encoding='utf-8') -> int:
        with open(path, flag, encoding=encoding) as f:
            _ret = f.write(data)
        return _ret

