# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : uri_app.py
# ------------------------------------------------------------------------------
#
# File          : uri_app.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import typing
import addict, blinker
from framework.application.urlobject import URLObject


class AppURI:
    sigUriQueryChanged = blinker.signal('sigUriQueryChanged')

    def __init__(self, uri_path, scheme='app', parent=None):
        self.parent = parent
        self._uri = URLObject(uri_path)
        self._uri=self._uri.with_scheme(scheme)

    @property
    def uri(self):
        return self._uri

    @property
    def uri_scheme(self):
        return self._uri.scheme()

    @property
    def uri_path(self):
        return self._uri.path()

    @staticmethod
    def query2dict(uri: typing.Union[str, URLObject]):
        if isinstance(uri, str):
            uri = URLObject(uri)
        return addict.Dict(uri.query_dict)

    @staticmethod
    def query2dict_qsl(uri: typing.Union[str, URLObject]):
        if isinstance(uri, str):
            uri = URLObject(uri)
        return addict.Dict(uri.query_multi_dict)

    def clear(self):
        """
        method to clear all query from this URI
        """
        self._uri.with_query(None)

    def has_query(self, key: str):
        return key in self.query2dict(self._uri)

    def set_query(self, *args, **kwargs):
        """
        method to set the query by given QUrlQuery instance or dict.
        the dict allow the duplicate key not, so use dict to set the query is little disadvantage.
        """

        self._uri.add_query_params(*args,**kwargs)
        self.sigUriQueryChanged.send(self)

    def append_query(self, key, value, allow_duplicate=False, emit=True):
        """
        method to append a query into this URI.
        if allow_duplicate is True, there is maybe a URI has duplicated value.
        """
        _old_query = self.query2dict(self._uri)
        if key in _old_query:
            if allow_duplicate:
                self._uri.with_query('%s=%s'%(key,value))
            else:
                return
        else:
            self._uri.add_query_param(key, value)
        if emit:
            self.sigUriQueryChanged.emit()

    def append_queries(self, lst: list, allow_duplicate=False):
        """
        method to append batch query by given list
        item of list in format (key,value) required.
        """
        for k, v in lst:
            self.append_query(k, v, allow_duplicate, emit=False)
        self.sigUriQueryChanged.emit()

    def remove_query(self, key: str, value: str = None, emit=True):
        """
        method to remove query by given key or value.
        if value is not None, then only the key and value considered item will be removed.
        otherwise the all key equal the given key will be removed.
        """
        _old_query = self.query2dict(self._uri)
        if key not in _old_query:
            return
        self._uri.del_query_param(key)
        if emit:
            self.sigUriQueryChanged.emit()

    def remove_queries(self, lst: list):
        """
        method to remove batch query by given list
        item of list in format (key,value) required.
        """
        for k, v in lst:
            self.remove_query(k, v, False)
        self.sigUriQueryChanged.emit()
