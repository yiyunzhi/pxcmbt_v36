# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       :
# Sourcefile(s) : class_ipod.py
# ------------------------------------------------------------------------------
#
# File          : class_ipod.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import anytree


class CoverageResolver:
    def __init__(self):
        pass

    def generate(self):
        pass


class DataConstraint:
    pass


class IPOD:
    def __init__(self):
        self.uuid = 0
        self.iod = None
        self.processor = None
        self.reversion = 0
        self.dependencies = None

    def resolve(self):
        """
        resolve the output based on it own input and processor.
        Returns:

        """
        pass


# todo: IPOD as tree implemented not processor.
class IPODProcessor(anytree.NodeMixin):
    # STC,FUNC,BT, isGraphic
    def __init__(self):
        pass

    def make_graph(self):
        pass
