# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_mapped_image_list.py
# ------------------------------------------------------------------------------
#
# File          : class_mapped_image_list.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx


class MappedImageList(wx.ImageList):
    def __init__(self, width=16, height=16, mask=True, initial_count=1, default=wx.ART_NORMAL_FILE):
        wx.ImageList.__init__(self, width, height, mask, initial_count)
        self._idxMap = dict()
        self._nameMap = dict()
        self.defaultArt = default
        self.initialize()

    @property
    def idxMap(self):
        return self._idxMap

    @property
    def nameMap(self):
        return self._nameMap

    def add_index_map(self, idx: int, name: str):
        self._nameMap.update({idx: name})
        self._idxMap.update({name: idx})

    def name2index(self, name: str) -> int:
        return self._idxMap.get(name)

    def index2name(self, idx: int) -> str:
        return self._nameMap.get(idx)

    def initialize(self):
        raise NotImplementedError
