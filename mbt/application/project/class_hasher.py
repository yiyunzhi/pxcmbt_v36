# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_hasher.py
# ------------------------------------------------------------------------------
#
# File          : class_hasher.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import hashlib, typing,pickle
from .class_project import ProjectTreeNode


class ProjectNodeHasher:
    @staticmethod
    def get_hash(*args, string=True):
        _hashed = hashlib.md5(pickle.dumps(args))
        return _hashed if not string else _hashed.hexdigest()

    @staticmethod
    def hash_node(node: ProjectTreeNode,use_workbench=False):
        _uri=str(node.stereotypeUri)
        if use_workbench:
            return ProjectNodeHasher.get_hash(node.workbenchUid,node.role, _uri)
        else:
            return ProjectNodeHasher.get_hash(node.role, _uri)
