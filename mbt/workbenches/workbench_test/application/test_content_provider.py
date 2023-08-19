# -*- coding: utf-8 -*-
import dataclasses

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : reqrepo_content_provider.py
# ------------------------------------------------------------------------------
#
# File          : reqrepo_content_provider.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.application.content_resolver import ContentContract
from framework.application.io import AppFileIO
from mbt.application.project import WorkFileNode
from mbt.application.workbench_base import MBTProjectOrientedWorkbench,MBTWorkbenchProjectContentProvider
from .define import WB_TEST_UID


class TestContentProviderException(Exception): pass


@dataclasses.dataclass
class TestContentInsertContract(ContentContract):
    uid: str
    name: str
    path: str = ''
    extension: str = '.obj'
    permission: str = 'RW'
    action: str = 'insert'
    workbench: str = WB_TEST_UID


@dataclasses.dataclass
class TestContentQueryContract(ContentContract):
    name: str
    uid: str
    path: str
    extension: str = '.obj'
    action: str = 'query'
    workbench: str = WB_TEST_UID

    def get_work_file_node_uri(self):
        return WorkFileNode.get_uri(path=self.path, name=self.name, ext=self.extension)


@dataclasses.dataclass
class TestContentNodeQueryContract(ContentContract):
    """
    contact contains a callback function for filtering the nodes.
    this callable function accept an argument etc. the root node of current project only.
    """
    action: callable
    workbench: str = WB_TEST_UID


@dataclasses.dataclass
class TestContentUpdateContract(ContentContract):
    name: str
    uid: str
    path: str
    extension: str = '.obj'
    action: str = 'update'
    workbench: str = WB_TEST_UID

    def get_work_file_node_uri(self):
        return WorkFileNode.get_uri(path=self.path, name=self.name, ext=self.extension)


@dataclasses.dataclass
class TestContentDeleteContract(ContentContract):
    name: str
    uid: str
    path: str
    extension: str = '.obj'
    action: str = 'delete'
    workbench: str = WB_TEST_UID

    def get_work_file_node_uri(self):
        return WorkFileNode.get_uri(path=self.path, name=self.name, ext=self.extension)


class TestContentProvider(MBTWorkbenchProjectContentProvider):

    def __init__(self, workbench: MBTProjectOrientedWorkbench, **kwargs):
        MBTWorkbenchProjectContentProvider.__init__(self, workbench, **kwargs)
        assert workbench.uid == WB_TEST_UID, TypeError('Workbench UID mismatched.')

    def insert(self, contract: TestContentInsertContract) -> bool:
        """
        Args:
            contract:ContentContract

        Returns:

        """
        assert isinstance(contract, TestContentInsertContract), TestContentProviderException('type TestContentInsertContract required.')
        assert contract.workbench==self.workbench.uid,TestContentProviderException('invalid contract uid.')
        return self.workbench.do_content_insert(contract)

    def update(self, contract: TestContentUpdateContract) -> bool:
        assert isinstance(contract, TestContentUpdateContract), TestContentProviderException('type TestContentUpdateContract required.')
        assert contract.workbench == self.workbench.uid, TestContentProviderException('invalid contract uid.')
        return self.workbench.do_content_update(contract)

    def delete(self, contract: TestContentDeleteContract) -> bool:
        assert isinstance(contract, TestContentDeleteContract), TestContentProviderException('type TestContentDeleteContract required.')
        assert contract.workbench == self.workbench.uid, TestContentProviderException('invalid contract uid.')
        return self.workbench.do_content_delete(contract)

    def query(self, contract: TestContentQueryContract) -> AppFileIO:
        assert isinstance(contract, (TestContentQueryContract, TestContentNodeQueryContract)), \
            TestContentProviderException('type TestContentQueryContract required.')
        assert contract.workbench == self.workbench.uid, TestContentProviderException('invalid contract uid.')
        return self.workbench.do_content_query(contract)
