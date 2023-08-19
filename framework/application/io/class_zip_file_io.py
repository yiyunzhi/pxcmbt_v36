# -*- coding: utf-8 -*-
import os
# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_zip_file_io.py
# ------------------------------------------------------------------------------
#
# File          : class_zip_file_io.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import os
import zipfile
from .class_base import AppFileIO


class ZipFileIO(AppFileIO):
    """
    no compression just for store the data in zip
    """
    def __init__(self, **kwargs):
        AppFileIO.__init__(self, **kwargs)
        self.extension = kwargs.get('extension', '.ioz')
        self._nameList = []

    @property
    def nameList(self):
        return self.nameList

    def read(self, extract_to=None, extract_files=None):
        _path = self.get_full_path()
        with zipfile.ZipFile(_path) as zf:
            self._nameList = zf.namelist()
            if extract_to is not None:
                assert os.path.exists(extract_to)
                if extract_files is not None:
                    for x in extract_files:
                        zf.extract(x, extract_to)
                else:
                    zf.extractall(extract_to)

    def write(self, files: list,relative=True):
        assert all([os.path.exists(x) for x in files])
        _path = self.get_full_path()
        with zipfile.ZipFile(_path,'w') as zf:
            for x in files:
                if relative:
                    _arcname=os.path.relpath(x,self.filePath)
                else:
                    _arcname=None
                zf.write(x,_arcname)
        return _path
