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
import wx
from framework import appCtxRegistry
from .application.class_application import MBTApplication
from .application.class_application_context import MBTApplicationContext
from .application.project import EnumProjectItemRole, ProjectNodeEditorTypeFactoryItem, ProjectTreeNode
from .workbenches.workbench_model import ModelWorkbench, ModelContentProvider
from .workbenches.workbench_reqrepo import ReqRepoWorkbench, ReqRepoContentProvider
from .workbenches.workbench_test import TestWorkbench, TestContentProvider

appCtx: MBTApplicationContext = MBTApplicationContext()


def setup_application_context(app: MBTApplication):
    # register app context.
    appCtx.setup(app)
    appCtxRegistry.register(appCtx)
    # register builtin workbench.
    _editor_registry_item_class = ProjectNodeEditorTypeFactoryItem
    _model_wb = ModelWorkbench(base_role=EnumProjectItemRole.MODEL.value)
    _test_wb = TestWorkbench(base_role=EnumProjectItemRole.TEST.value)
    _req_wb = ReqRepoWorkbench(base_role=EnumProjectItemRole.REQ_MGR.value)

    app.workbenchRegistry.register_workbench(_model_wb)
    app.workbenchRegistry.register_workbench(_test_wb)
    app.workbenchRegistry.register_workbench(_req_wb)

    app.baseContentResolver.register(TestContentProvider(_test_wb))
    app.baseContentResolver.register(ModelContentProvider(_model_wb))
    app.baseContentResolver.register(ReqRepoContentProvider(_req_wb))
