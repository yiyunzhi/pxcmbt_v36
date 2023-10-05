# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_workbench_view_manager.py
# ------------------------------------------------------------------------------
#
# File          : class_workbench_view_manager.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx, copy
from framework.application.utils_helper import util_generate_uri
from framework.gui.base import FeedbackDialogs
from mbt.application.define import EnumAppSignal
from mbt.application.project import EnumProjectItemRole, ProjectTreeNode, ProjectNodeProfile
from mbt.application.workbench_base import MBTBaseWorkbenchViewManager
from mbt.gui.base import MBTUniView
from mbt.gui.project import UtilProjectNodeEdit
from .application.class_base_cc import (ModelWorkbenchBaseContentContainer,
                                        CommandAppendProjectNode,
                                        CommandRemoveProjectNode,
                                        CommandModifyProjectNodeProperty)
from .gui.class_view import ModelWorkbenchMainView
from .gui.define import EnumModelWorkbenchMenuIds
from .class_app_toolbar_mgr import WBProcessToolbarViewManager


class MBTModelWorkbenchViewManager(MBTBaseWorkbenchViewManager):
    def __init__(self, **kwargs):
        MBTBaseWorkbenchViewManager.__init__(self, **kwargs)
        self._viewTitle = 'Model'
        self._processToolbarViewMgr = WBProcessToolbarViewManager(parent=self, uid='%s_ptb' % self.uid)
        # todo: could more toolbars
        EnumAppSignal.sigProjectNodeSelectChanged.connect(self.on_app_sig_project_node_select_changed)

    def create_view(self, **kwargs) -> MBTUniView:
        # _main_view = ModelWorkbenchMainView(manager=self)
        if self._processToolbarViewMgr.view is None:
            _view = self._processToolbarViewMgr.create_view(**kwargs)
            _view.Bind(wx.EVT_MENU, self.on_menu)
        _base_cc = ModelWorkbenchBaseContentContainer(manager=self)
        self.post_content_container(_base_cc)
        # return _main_view

    def setup(self, *args, **kwargs):
        """
        will be triggerd if any project open or created.
        Args:
            *args:
            **kwargs:

        Returns:

        """
        self.log.debug('%s setup.' % '/'.join([x.uid for x in self.path]))
        _view_parent = self.root.view
        self.create_view(parent=_view_parent)
        self._processToolbarViewMgr.set_init_state()

    def teardown(self, *args, **kwargs):
        self.log.debug('%s teardown.' % '/'.join([x.uid for x in self.path]))
        self._processToolbarViewMgr.remove_view()

    def prepare_add_node(self, parent: ProjectTreeNode, child_role: str, describable: bool, role_name: str, **kwargs) -> (bool, dict):
        _auto_name = ProjectTreeNode.auto_generate_name(parent, role_name)
        _init_param = {'profile':
                           {'name': _auto_name,
                            'description': 'description of %s' % role_name
                            },
                       'role': child_role
                       }
        if describable:
            _wz_options = dict()
            _wz_options['title'] = 'New%sNode' % role_name
            _wz_options['profile_content'] = _init_param['profile']
            _solution_choice = False
            _wb_uid = parent.workbenchUid
            if child_role == EnumProjectItemRole.BEHAVIOUR.value:
                _solution_choice = True
                _app = wx.App.GetInstance()
                _slt_mgr = _app.mbtSolutionManager
                _slts = {x.name: (x.uuid, x.type_) for x in _slt_mgr.solutions.values() if x.isValid}
                _slt_descs = {v.name: v.description for v in _slt_mgr.solutions.values() if v.isValid}
                _bmps = {x.name: x.iconInfo[1] for x in _slt_mgr.solutions.values() if x.isValid}
                _wz_options['choice_content'] = {'choices': list(_slts.keys()),
                                                 'bmps': list(_bmps.values()),
                                                 'descriptions': _slt_descs}
                _wz_options['choice_title'] = 'Select Solution'
                _wz_options['choice_description'] = 'Select a solution from given list.'
                _wz_options['choice_label'] = 'Solution:'
            _ret, _res = UtilProjectNodeEdit.wizard_for_new_or_edit_node(**_wz_options)
            if _ret:
                if _solution_choice:
                    _slt_uid, _slt_typ = _slts[_res['selected']]
                    _res['icon'] = _bmps[_res['selected']]
                    _res.update({
                        'stereotype': ProjectTreeNode.NODE_ST_SOLUTION,
                        'stereotypeQuery': {
                            'name': _slt_typ,
                            'uid': _slt_uid,
                        }
                    })
                    _res.pop('selected')
                _res['profile'] = ProjectNodeProfile(**_res['profile'])
                _res['role'] = child_role
            return _ret, _res
        else:
            _res = copy.deepcopy(_init_param)
            _res.update({'profile': ProjectNodeProfile(**_init_param['profile'])})
            return True, _res

    def add_project_node(self, parent_node: ProjectTreeNode, meta: dict, role_name: str, copy_=False):
        if copy_:
            _name = 'ModelWorkbenchCopy%sNode' % role_name
        else:
            _name = 'ModelWorkbenchAddNew%sNode' % role_name
        _cmd = CommandAppendProjectNode(self, parent_node.uuid, meta, name=_name)
        _ret = self.undoStack.Submit(_cmd)
        if _ret:
            return _ret, _cmd.nodeUid
        else:
            return _ret, 'undostack command could not executed successfully.'

    def remove_project_node(self, node: ProjectTreeNode):
        _cmd = CommandRemoveProjectNode(self, node, name='ModelWorkbenchRemove%sNode' % node.label)
        _ret = self.undoStack.Submit(_cmd)
        if _ret:
            return _ret, _cmd.node
        else:
            return _ret, 'undostack command could not executed successfully.'

    def modify_node_property(self, node: ProjectTreeNode, modifier_key: str):
        if modifier_key == ProjectTreeNode.MODIFIER_KEY_PROFILE:
            _wz_options = dict()
            _wz_options['title'] = 'Reprofile %s' % node.label
            _wz_options['profile_content'] = {'name': node.profile.get('name'), 'description': node.profile.get('description')}
            _ret, _res = UtilProjectNodeEdit.wizard_for_new_or_edit_node(**_wz_options)
            if _ret:
                _cmd = CommandModifyProjectNodeProperty(self, node,
                                                        name='ModelWorkbenchModify%sNode' % node.label,
                                                        new_value=_res['profile'], old_value=_wz_options['profile_content'], modifier_key=modifier_key)
                _ret = self.undoStack.Submit(_cmd)
                if _ret:
                    return _ret, _cmd.node
                else:
                    return _ret, 'undostack command could not executed successfully.'
        else:
            return False, 'unsupported modifier key %s' % modifier_key

    # --------------------------------------------------------------
    # event handling
    # --------------------------------------------------------------
    def on_app_sig_project_node_select_changed(self, sender, node: ProjectTreeNode):
        self._processToolbarViewMgr.set_init_state()
        if not self.workbench.is_my_descendant(node.role, 'role'):
            self._processToolbarViewMgr.refresh_view()
            return
        if node.role in [EnumProjectItemRole.PROTOTYPE.value,
                         EnumProjectItemRole.PROTOTYPE_SKETCH.value,
                         EnumProjectItemRole.BEHAVIOUR.value]:
            self._processToolbarViewMgr.set_state(EnumModelWorkbenchMenuIds.DEBUG, True)
        elif node.role in [EnumProjectItemRole.PROTOTYPE.value,
                           EnumProjectItemRole.PROTOTYPE_SKETCH.value]:
            self._processToolbarViewMgr.set_state(EnumModelWorkbenchMenuIds.BUILD, True)
        self._processToolbarViewMgr.refresh_view()

    def on_menu(self, evt: wx.CommandEvent):
        _id = evt.GetId()
        if _id == EnumModelWorkbenchMenuIds.BUILD:
            FeedbackDialogs.show_msg_dialog('todo', 'build model')
        elif _id == EnumModelWorkbenchMenuIds.DEBUG:
            FeedbackDialogs.show_msg_dialog('todo', 'debug model')
