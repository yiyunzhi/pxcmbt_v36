# -*- coding: utf-8 -*-
import dataclasses
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
from dataclasses import dataclass, field
from framework.application.urlobject import URLObject
from framework.application.content_provider import ContentProvider


class ContentResolverException(Exception): pass


class ResolverContext:
    def __init__(self):
        self._consumers = set()


@dataclass
class ContentContract:
    uri: str
    data: object


class ContentResolver:
    def __init__(self):
        self._providers = dict()
        self._resolverContexts = dict()

    def register(self, provider: ContentProvider, override=False):
        """
        register a provider into this solver.

        Args:
            provider: ContentProvider
            override: bool, use this argument could lose the previous reference

        Returns:

        """
        _base_uri = provider.baseUri
        _exist=self._providers.get(_base_uri)
        if _exist and not override:
            raise ContentResolverException('provider with base uri %s already exist.' % _base_uri)
        if _exist and not _exist.overrideable:
            raise ContentResolverException('provider with base uri %s is not overrideable.' % _base_uri)
        provider.resolver = self
        self._providers.update({_base_uri: provider})
        self._resolverContexts.update({_base_uri: ResolverContext()})
        return provider

    def unregister(self, authority_or_uri: str):
        _uri = URLObject(authority_or_uri)
        if _uri.scheme != ContentProvider.SCHEME:
            _uri = ContentProvider.build_uri(authority_or_uri)
        else:
            _uri = authority_or_uri
        if _uri in self._providers:
            self._providers.pop(_uri)
        if _uri in self._resolverContexts:
            self._resolverContexts.pop(_uri)

    def unregister_by_type(self, type_: type):
        _l = list()
        for k, v in self._providers.items():
            if isinstance(v, type_):
                _l.append(k)
        [self.unregister(x) for x in _l]

    @staticmethod
    def check_uri(uri) -> bool:
        if uri is None:
            return False
        _uri = URLObject(uri)
        return _uri.scheme == ContentProvider.SCHEME

    @staticmethod
    def get_base_uri(uri) -> str:
        _uri = URLObject(uri)
        _uri2 = URLObject()
        _uri2 = _uri.with_scheme(_uri.scheme)
        _uri2 = _uri.with_path(_uri.path)
        return str(_uri2)

    def get_provider(self, uri) -> typing.Union[None, ContentProvider]:
        if not self.check_uri(uri):
            return None
        return self._providers.get(self.get_base_uri(uri))

    def insert(self, contract: ContentContract) -> bool:
        """
        method insert data into provider, which by uri indicated.
        Args:
            contract: ContentContract

        Returns: bool

        """
        _provider = self.get_provider(contract.uri)
        if _provider is None:
            return False
        return _provider.insert(contract)

    def update(self, contract: ContentContract) -> bool:
        """
        method update data into provider, which by uri indicated
        Args:
            contract: ContentContract

        Returns: bool

        """
        _provider = self.get_provider(contract.uri)
        if _provider is None:
            return False
        return _provider.update(contract)

    def delete(self, contract: ContentContract) -> bool:
        """
        method delete data from provider, which by uri indicated
        Args:
            contract: ContentContract

        Returns: bool

        """
        _provider = self.get_provider(contract.uri)
        if _provider is None:
            return False
        return _provider.delete(contract)

    def query(self, contract: ContentContract) -> object:
        """
        method query data from provider, which by uri indicated
        Args:
            contract: ContentContract

        Returns: object

        """
        _provider = self.get_provider(contract.uri)
        if _provider is None:
            return None
        return _provider.query(contract)
