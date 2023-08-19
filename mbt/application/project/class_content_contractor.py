# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_content_contractor.py
# ------------------------------------------------------------------------------
#
# File          : class_content_contractor.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from .project_content_provider import (ProjectContentProvider,
                                       ContentContract,
                                       ProjectContentDeleteContract,
                                       ProjectContentInsertContract,
                                       ProjectContentUpdateContract,
                                       ProjectContentQueryContract, ProjectContentNodeQueryContract)


class ProjectContentContractor:
    def __init__(self):
        self._contentUri = ProjectContentProvider.build_uri(ProjectContentProvider.AUTHORITY)

    def build_insert_contract(self, uid: str, name: str, path: str = '', extension: str = '.obj', data: object = None):
        """
        Args:
            uid: str, uuid of projectNode.
            name: str, the file name for storing.
            path: str, the node's path, like a\b if you wanna store data in a\b folder.
            extension: str, the extension of filename for storing
            data: object, in principle should be serializable

        Returns: ProjectContentInsertContract
        """
        return ProjectContentInsertContract(uri=self._contentUri,
                                            data=data,
                                            path=path,
                                            uid=uid,
                                            name=name, extension=extension)

    def build_update_contract(self, uid: str, name: str, path: str = '', extension: str = '.obj', data: object = None):
        """
        Args:
            uid: str, uuid of projectNode.
            name: str, the file name for storing.
            path: str, the node's path, like a\b if you wanna store data in a\b folder.
            extension: str, the extension of filename for storing
            data: object, in principle should be serializable

        Returns: ProjectContentUpdateContract
        """
        return ProjectContentUpdateContract(uri=self._contentUri,
                                            data=data,
                                            name=name, extension=extension,
                                            uid=uid, path=path)

    def build_query_contract(self, uid: str, name: str, path: str = '', extension: str = '.obj'):
        """
        Args:
            uid: str, uuid of projectNode.
            name: str, the file name for storing.
            path: str, the node's path, like a\b if you wanna store data in a\b folder.
            extension: str, the extension of filename for storing

        Returns: ProjectContentQueryContract
        """
        return ProjectContentQueryContract(uri=self._contentUri,
                                           data=None,
                                           name=name, extension=extension,
                                           uid=uid, path=path)

    def build_node_query_contract(self, action: callable):
        """
        Args:
            action: callable object.

        Returns: ProjectContentNodeQueryContract
        """
        return ProjectContentNodeQueryContract(uri=self._contentUri, action=action, data=None)

    def build_delete_contract(self, uid: str, name: str, path: str = '', extension: str = '.obj'):
        """
        Args:
            uid: str, uuid of projectNode.
            name: str, the file name for storing.
            path: str, the node's path, like a\b if you wanna store data in a\b folder.
            extension: str, the extension of filename for storing

        Returns: ProjectContentDeleteContract
        """
        return ProjectContentDeleteContract(uri=self._contentUri,
                                            data=None,
                                            name=name, extension=extension,
                                            uid=uid, path=path)
