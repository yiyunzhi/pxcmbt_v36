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
from .define import WB_REQ_REPO_UID


class ReqRepoContentProviderException(Exception): pass


@dataclasses.dataclass
class ReqRepoContentInsertContract(ContentContract):
    uid: str
    name: str
    path: str = ''
    extension: str = '.obj'
    permission: str = 'RW'
    action: str = 'insert'
    workbench: str = WB_REQ_REPO_UID


@dataclasses.dataclass
class ReqRepoContentQueryContract(ContentContract):
    name: str
    uid: str
    path: str
    extension: str = '.obj'
    action: str = 'query'
    workbench: str = WB_REQ_REPO_UID

    def get_work_file_node_uri(self):
        return WorkFileNode.get_uri(path=self.path, name=self.name, ext=self.extension)


@dataclasses.dataclass
class ReqRepoContentNodeQueryContract(ContentContract):
    """
    contact contains a callback function for filtering the nodes.
    this callable function accept an argument etc. the root node of current project only.
    """
    action: callable
    workbench: str = WB_REQ_REPO_UID


@dataclasses.dataclass
class ReqRepoContentUpdateContract(ContentContract):
    name: str
    uid: str
    path: str
    extension: str = '.obj'
    action: str = 'update'
    workbench: str = WB_REQ_REPO_UID

    def get_work_file_node_uri(self):
        return WorkFileNode.get_uri(path=self.path, name=self.name, ext=self.extension)


@dataclasses.dataclass
class ReqRepoContentDeleteContract(ContentContract):
    name: str
    uid: str
    path: str
    extension: str = '.obj'
    action: str = 'delete'
    workbench: str = WB_REQ_REPO_UID

    def get_work_file_node_uri(self):
        return WorkFileNode.get_uri(path=self.path, name=self.name, ext=self.extension)


class ReqRepoContentProvider(MBTWorkbenchProjectContentProvider):

    def __init__(self, workbench: MBTProjectOrientedWorkbench, **kwargs):
        MBTWorkbenchProjectContentProvider.__init__(self, workbench, **kwargs)
        assert workbench.uid == WB_REQ_REPO_UID, TypeError('Workbench UID mismatched.')

    def insert(self, contract: ReqRepoContentInsertContract) -> bool:
        """
        Args:
            contract:ContentContract

        Returns:

        """
        assert isinstance(contract, ReqRepoContentInsertContract), ReqRepoContentProviderException('type ReqRepoContentInsertContract required.')
        assert contract.workbench==self.workbench.uid,ReqRepoContentProviderException('invalid contract uid.')
        return self.workbench.do_content_insert(contract)

    def update(self, contract: ReqRepoContentUpdateContract) -> bool:
        assert isinstance(contract, ReqRepoContentUpdateContract), ReqRepoContentProviderException('type ReqRepoContentUpdateContract required.')
        assert contract.workbench == self.workbench.uid, ReqRepoContentProviderException('invalid contract uid.')
        return self.workbench.do_content_update(contract)

    def delete(self, contract: ReqRepoContentDeleteContract) -> bool:
        assert isinstance(contract, ReqRepoContentDeleteContract), ReqRepoContentProviderException('type ReqRepoContentDeleteContract required.')
        assert contract.workbench == self.workbench.uid, ReqRepoContentProviderException('invalid contract uid.')
        return self.workbench.do_content_delete(contract)

    def query(self, contract: ReqRepoContentQueryContract) -> AppFileIO:
        assert isinstance(contract, (ReqRepoContentQueryContract, ReqRepoContentNodeQueryContract)), \
            ReqRepoContentProviderException('type ReqRepoContentQueryContract required.')
        assert contract.workbench == self.workbench.uid, ReqRepoContentProviderException('invalid contract uid.')
        return self.workbench.do_content_query(contract)
