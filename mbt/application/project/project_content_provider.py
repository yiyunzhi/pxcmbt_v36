# -*- coding: utf-8 -*-
import dataclasses

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : project_content_provider.py
# ------------------------------------------------------------------------------
#
# File          : project_content_provider.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.application.content_provider import ContentProvider
from framework.application.content_resolver import ContentContract
from framework.application.urlobject import URLObject
from framework.application.io import AppFileIO
from mbt.application.base import MBTContentContainer
from .class_file_resolver import WorkFileNode


class ProjectContentProviderException(Exception): pass


@dataclasses.dataclass
class ProjectContentInsertContract(ContentContract):
    uid: str
    name: str
    path: str = ''
    extension: str = '.obj'
    permission: str = 'RW'
    action: str = 'insert'


@dataclasses.dataclass
class ProjectContentQueryContract(ContentContract):
    name: str
    uid: str
    path: str
    extension: str = '.obj'
    action: str = 'query'

    def get_work_file_node_uri(self):
        return WorkFileNode.get_uri(path=self.path, name=self.name, ext=self.extension)


@dataclasses.dataclass
class ProjectContentNodeQueryContract(ContentContract):
    """
    contact contains a callback function for filtering the nodes.
    this callable function accept an argument etc. the root node of current project only.
    """
    action: callable


@dataclasses.dataclass
class ProjectContentUpdateContract(ContentContract):
    name: str
    uid: str
    path: str
    extension: str = '.obj'
    action: str = 'update'

    def get_work_file_node_uri(self):
        return WorkFileNode.get_uri(path=self.path, name=self.name, ext=self.extension)


@dataclasses.dataclass
class ProjectContentDeleteContract(ContentContract):
    name: str
    uid: str
    path: str
    extension: str = '.obj'
    action: str = 'delete'

    def get_work_file_node_uri(self):
        return WorkFileNode.get_uri(path=self.path, name=self.name, ext=self.extension)


class ProjectContentProvider(ContentProvider):
    AUTHORITY = 'project'
    VERSION = '1.0.0'

    def __init__(self, content_container: MBTContentContainer, **kwargs):
        ContentProvider.__init__(self, **kwargs, authority=self.AUTHORITY)
        self.contentContainer = content_container
        assert isinstance(self.contentContainer, MBTContentContainer), TypeError('MBTContentContainer type is required.')

    def insert(self, contract: ProjectContentInsertContract) -> bool:
        """
        Args:
            contract:ContentContract

        Returns:

        """
        assert isinstance(contract, ProjectContentInsertContract), ProjectContentProviderException('type ProjectContentInsertContract required.')
        return self.contentContainer.set(contract)

    def update(self, contract: ProjectContentUpdateContract) -> bool:
        assert isinstance(contract, ProjectContentUpdateContract), ProjectContentProviderException('type ProjectContentUpdateContract required.')
        return self.contentContainer.set(contract)

    def delete(self, contract: ProjectContentDeleteContract) -> bool:
        assert isinstance(contract, ProjectContentDeleteContract), ProjectContentProviderException('type ProjectContentDeleteContract required.')
        return self.contentContainer.set(contract)

    def query(self, contract: ProjectContentQueryContract) -> AppFileIO:
        assert isinstance(contract, (ProjectContentQueryContract,ProjectContentNodeQueryContract)), \
            ProjectContentProviderException('type ProjectContentQueryContract required.')
        return self.contentContainer.get(contract)
