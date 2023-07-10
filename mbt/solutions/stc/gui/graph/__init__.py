# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : __init__.py.py
# ------------------------------------------------------------------------------
#
# File          : __init__.py.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------

from .factory import SOLUTION_STC_CLS_FACTORY
from .graph import STCNodeGraph
from .nodes import InitialStateNode, FinalStateNode, SimpleStateNode, CompositeStateNode, SubStateNode
from .node_items import FinalStateViewItem, InitialStateViewItem, SimpleStateViewItem, SubStateViewItem, CompositeStateViewItem
from .pipe import STCLivePipeObject, STCPipeObject
from .pipe_items import STCPipeViewItem, STCLivePipeViewItem
from .view import STCGraphView
from .graph_interactor import STCGraphEditInteractor,STCGraphConnectInteractor
from .define import *


SOLUTION_STC_CLS_FACTORY.register(STCGraphView)
SOLUTION_STC_CLS_FACTORY.register(FinalStateViewItem)
SOLUTION_STC_CLS_FACTORY.register(InitialStateViewItem)
SOLUTION_STC_CLS_FACTORY.register(SimpleStateViewItem)
SOLUTION_STC_CLS_FACTORY.register(SubStateViewItem)
SOLUTION_STC_CLS_FACTORY.register(CompositeStateViewItem)
SOLUTION_STC_CLS_FACTORY.register(STCPipeViewItem)
SOLUTION_STC_CLS_FACTORY.register(STCLivePipeViewItem)