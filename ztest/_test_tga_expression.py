# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _test_tga_expression.py
# ------------------------------------------------------------------------------
#
# File          : _test_tga_expression.py
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
app=wx.App()
from mbt.solutions.stc.diagram.class_element_userdata import BaseElementUserdata
from framework.application.urlobject import URLObject


class TGAExpression(BaseElementUserdata):
    serializeTag = '!TGAExpression'
    # todo: make this serializable
    EXPR_FORMAT = '{}/[{}]/{}'
    ELIDE_LENGTH = 10

    def __init__(self, **kwargs):
        BaseElementUserdata.__init__(self, **kwargs)
        # elide?
        self.tScheme = 'T'
        self.gScheme = 'G'
        self.aScheme = 'A'
        _t_url = URLObject()
        _t_url = _t_url.with_scheme(self.tScheme)
        _t_url = _t_url.set_query_params(**{'ref': 'a', 'code': 'evt_setV', 'uuid': ''})
        self.tUri = _t_url
        _g_url = URLObject()
        _g_url = _g_url.with_scheme(self.gScheme)
        _g_url = _g_url.set_query_params(**{'ref': 'a', 'code': 'au_tz_45==10', 'uuid': ''})
        self.gUri = _g_url
        _a_url = URLObject()
        _a_url = _a_url.with_scheme(self.aScheme)
        _a_url = _a_url.set_query_params(**{'ref': 'b', 'code': 'flashLed()', 'uuid': '45ttzwd78'})
        self.aUri = _a_url

    @property
    def serializer(self):
        _d = BaseElementUserdata.serializer.fget(self)
        _d.update({'tQueries': self.tUri.query_dict, 'gQueries': self.gUri.query_dict, 'aQueries': self.aUri.query_dict})
        return _d

    @property
    def expression(self):
        _texpr = self.tUri.query_dict.get('code')
        _gexpr = self.gUri.query_dict.get('code')
        _aexpr = self.aUri.query_dict.get('code')
        return self.EXPR_FORMAT.format(_texpr, _gexpr, _aexpr)

    def set_trigger(self, queries: dict):
        self.tUri.set_query_params(**queries)

    def set_guard(self, queries: dict):
        self.gUri.set_query_params(**queries)

    def set_action(self, queries: dict):
        self.aUri.set_query_params(**queries)


_expr = TGAExpression()
print(_expr.expression)
print(_expr.aUri.query_dict)
