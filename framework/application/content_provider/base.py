# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : base.py
# ------------------------------------------------------------------------------
#
# File          : base.py
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
from framework.application.urlobject import URLObject


class ContentProvider:
    """
    <prefix>://<authority>/<data_type>/<id>
    This prefix is always set to content://
    authority
        This specifies the name of the content provider, for example contacts, browser etc.
        For third-party content providers, this could be the fully qualified name,
        such as com.tutorialspoint.statusprovider
    data_type
        This indicates the type of data that this particular provider provides. For example,
        if you are getting all the contacts from the Contacts content provider, then the data
        path would be people and URI would look like this content://contacts/people
    id
        This specifies the specific record requested. For example,
        if you are looking for contact number 5 in the Contacts content provider then
        URI would look like this content://contacts/people/5.
    """
    SCHEME = 'content'

    def __init__(self, **kwargs):
        self.resolver = kwargs.get('resolver')
        self.authority = kwargs.get('authority')
        assert self.authority is not None, ValueError('authority must be not empty')
        self.permission = kwargs.get('permission', 'RW')
        self.overrideable = kwargs.get('overrideable', True)

    @property
    def baseUri(self) -> str:
        _uri = URLObject()
        _uri = _uri.with_scheme(self.SCHEME)
        _uri = _uri.with_path(self.authority)
        return str(_uri)

    @property
    def canRead(self) -> bool:
        return 'R' in self.permission

    @property
    def canWrite(self) -> bool:
        return 'W' in self.permission

    @property
    def hasChanged(self) -> bool:
        return False

    @staticmethod
    def build_uri(authority: str, **queries):
        _uri = URLObject()
        _uri = _uri.with_scheme(ContentProvider.SCHEME)
        _uri = _uri.with_path(authority)
        _uri.set_query_params(**queries)
        return str(_uri)

    def insert(self, *args, **kwargs) -> typing.Any:
        raise NotImplementedError

    def update(self, *args, **kwargs) -> typing.Any:
        raise NotImplementedError

    def delete(self, *args, **kwargs) -> typing.Any:
        raise NotImplementedError

    def query(self, *args, **kwargs) -> typing.Any:
        raise NotImplementedError
