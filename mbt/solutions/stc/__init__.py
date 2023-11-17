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
import os
from mbt.application.class_application_context import MBTApplicationContext
from mbt.solutions.stc.stc_mc import STCEditorManager

from mbt.solutions.stc.gui.stc_editor_view import STCEditorView


THIS_PATH = os.path.dirname(os.path.abspath(__file__))




# _elm_factory.register(CompositeStateElement.identity, 'CompositeStateElement', CompositeStateElement)


def setup(app_ctx: MBTApplicationContext):
    print('Solution STC setup.')
    pass
    # _z_vf = app_ctx.zViewFactory
    # _z_vf.register(_uuid, STCEditorView, STCEditorContentContainer, STCEditorManager)


SOLUTION_DEF = {
    'uuid': '12aab13d-bbae-4092-9ace-fb4c996293fd',
    # 'icon': [None, 'md5.state-machine'],
    'icon': [os.path.join(THIS_PATH, 'resources', 'image', 'slt_stc.png'), 'solution.slt_stc'],
    # if icon use local icon, then index0 must be the path to the image.the index1 is the solution.name of image file.
    'namespace': 'StateChart',
    'type': 'stc',
    'version': '1.0.1',
    'view': STCEditorView,
    'viewManager': STCEditorManager,
    'setup': setup,
    'builtinEntitiesPath': '',
    'description': 'Solution with SysMl in statechart for modeling.'
}
