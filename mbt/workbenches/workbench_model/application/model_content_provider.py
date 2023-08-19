# -*- coding: utf-8 -*-
import dataclasses

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : model_content_provider.py
# ------------------------------------------------------------------------------
#
# File          : model_content_provider.py
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
from mbt.application.workbench_base import MBTProjectOrientedWorkbench, MBTWorkbenchProjectContentProvider
from .define import WB_MODEL_UID


class ModelContentProviderException(Exception): pass


@dataclasses.dataclass
class ModelContentInsertContract(ContentContract):
    uid: str
    name: str
    path: str = ''
    extension: str = '.obj'
    permission: str = 'RW'
    action: str = 'insert'
    workbench: str = WB_MODEL_UID


@dataclasses.dataclass
class ModelContentQueryContract(ContentContract):
    name: str
    uid: str
    path: str
    extension: str = '.obj'
    action: str = 'query'
    workbench: str = WB_MODEL_UID

    def get_work_file_node_uri(self):
        return WorkFileNode.get_uri(path=self.path, name=self.name, ext=self.extension)


@dataclasses.dataclass
class ModelContentNodeQueryContract(ContentContract):
    """
    contact contains a callback function for filtering the nodes.
    this callable function accept an argument etc. the root node of current project only.
    """
    action: callable
    workbench: str = WB_MODEL_UID


@dataclasses.dataclass
class ModelContentUpdateContract(ContentContract):
    name: str
    uid: str
    path: str
    extension: str = '.obj'
    action: str = 'update'
    workbench: str = WB_MODEL_UID

    def get_work_file_node_uri(self):
        return WorkFileNode.get_uri(path=self.path, name=self.name, ext=self.extension)


@dataclasses.dataclass
class ModelContentDeleteContract(ContentContract):
    name: str
    uid: str
    path: str
    extension: str = '.obj'
    action: str = 'delete'
    workbench: str = WB_MODEL_UID

    def get_work_file_node_uri(self):
        return WorkFileNode.get_uri(path=self.path, name=self.name, ext=self.extension)


class ModelContentProvider(MBTWorkbenchProjectContentProvider):

    def __init__(self, workbench: MBTProjectOrientedWorkbench, **kwargs):
        MBTWorkbenchProjectContentProvider.__init__(self, workbench, **kwargs)
        assert workbench.uid == WB_MODEL_UID, TypeError('Workbench UID mismatched.')

    def insert(self, contract: ModelContentInsertContract) -> bool:
        """
        Args:
            contract:ContentContract

        Returns:

        """
        assert isinstance(contract, ModelContentInsertContract), ModelContentProviderException('type ModelContentInsertContract required.')
        assert contract.workbench == self.workbench.uid, ModelContentProviderException('invalid contract uid.')
        return self.workbench.do_content_insert(contract)

    def update(self, contract: ModelContentUpdateContract) -> bool:
        assert isinstance(contract, ModelContentUpdateContract), ModelContentProviderException('type ModelContentUpdateContract required.')
        assert contract.workbench == self.workbench.uid, ModelContentProviderException('invalid contract uid.')
        return self.workbench.do_content_update(contract)

    def delete(self, contract: ModelContentDeleteContract) -> bool:
        assert isinstance(contract, ModelContentDeleteContract), ModelContentProviderException('type ModelContentDeleteContract required.')
        assert contract.workbench == self.workbench.uid, ModelContentProviderException('invalid contract uid.')
        return self.workbench.do_content_delete(contract)

    def query(self, contract: ModelContentQueryContract) -> AppFileIO:
        assert isinstance(contract, (ModelContentQueryContract, ModelContentNodeQueryContract)), \
            ModelContentProviderException('type ModelContentQueryContract required.')
        assert contract.workbench == self.workbench.uid, ModelContentProviderException('invalid contract uid.')
        return self.workbench.do_content_query(contract)
