# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : solution.py
# ------------------------------------------------------------------------------
#
# File          : solution.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import os, wx
from addict import Dict


class MBTSolution:
    """
    solutionDef expect a dict likes:
        'icon': None,
        'namespace': 'StateChart',
        'type': 'stc',
        'version': '1.0.1',
        'editor': '',
    """
    EXPECT_DEF_KEY = ['icon', 'namespace', 'type', 'version', 'view','viewManager', 'builtinEntitiesPath', 'setup', 'uuid']

    def __init__(self, **kwargs):
        self._module = kwargs.get('module')
        assert self._module is not None
        self._modulePath = kwargs.get('module_path')
        _solutionDef = kwargs.get('solution_def', dict())
        assert all([k in _solutionDef for k in self.EXPECT_DEF_KEY])
        self._solutionDef = Dict(_solutionDef)

    @property
    def key(self):
        return '%s.%s' % (self.namespace, self.type_)

    @property
    def namespace(self):
        return self._solutionDef.get('namespace')

    @property
    def module_(self) -> str:
        return self._module

    @property
    def modulePath(self) -> str:
        return self._modulePath

    @property
    def solutionDef(self) -> dict:
        return self._solutionDef

    @property
    def isValid(self) -> bool:
        return self._solutionDef.get('setup') is not None

    @property
    def name(self) -> str:
        return '{} v{}'.format(self._solutionDef.get('namespace'), self._solutionDef.get('version'))

    @property
    def type_(self):
        return self._solutionDef.get('type')

    @property
    def description(self) -> str:
        return self._solutionDef.get('description')

    @property
    def uuid(self) -> str:
        return self._solutionDef['uuid']

    @property
    def viewClass(self) -> type:
        return self._solutionDef['view']

    @property
    def viewManagerClass(self) -> type:
        return self._solutionDef['viewManager']
    @property
    def iconInfo(self) -> str:
        return self._solutionDef.get('icon')

    def get_icon(self, size: wx.Size = wx.Size(16, 16)):
        _path, _icon = self.iconInfo
        if _path is not None:
            if os.path.exists(_path):
                _bmp = wx.Bitmap(_path, wx.BITMAP_TYPE_PNG)
                _bmp.Rescale(_bmp, size)
                return _bmp
            else:
                return wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, size)
        else:
            return wx.ArtProvider.GetBitmap(_icon, wx.ART_OTHER, size)

    def run_setup(self, app):
        if self.isValid:
            _setup = self._solutionDef.get('setup')
            if callable(_setup):
                _setup(app)
