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
import wx
import wx.lib.agw.aui as aui
from framework.application.utils_helper import util_generate_uri
from mbt.application.project import EnumProjectItemRole, ProjectTreeNode, ProjectNodeProfile
from mbt.application.workbench_base import MBTBaseWorkbenchViewManager
from mbt.gui.base import MBTUniView
from mbt.gui.project import UtilProjectNodeEdit
from .gui.class_view import ModelWorkbenchMainView
from .class_app_toolbar_mgr import WBProcessToolbarViewManager


class MBTModelWorkbenchViewManager(MBTBaseWorkbenchViewManager):
    def __init__(self, **kwargs):
        MBTBaseWorkbenchViewManager.__init__(self, **kwargs)
        self._viewTitle = 'Model'
        self._processToolbarViewMgr = WBProcessToolbarViewManager(parent=self, uid='%s_ptb' % self.uid)
        # todo: could more toolbars

    def create_view(self, **kwargs) -> MBTUniView:
        if self._processToolbarViewMgr.view is None:
            self._processToolbarViewMgr.create_view(**kwargs)
        return

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
        self._processToolbarViewMgr.remove_view()

    def prepare_add_node(self, role: str, describable: bool, role_name: str):
        if describable:
            _wz_options = dict()
            _wz_options['title'] = 'New%sNode' % role_name
            _wz_options['profile_content'] = {'name': 'New%s' % role_name, 'description': 'description of %s' % role_name}
            _solution_choice = False

            if role == EnumProjectItemRole.BEHAVIOUR.value:
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
                    _res.update({'stereotypeUri': util_generate_uri(ProjectTreeNode.NODE_STEREOTYPE_URI_SCHEME,
                                                                    uri_netloc='solution',
                                                                    name=_slt_typ,
                                                                    uid=_slt_uid)})
                    _res.pop('selected')
                _res['profile'] = ProjectNodeProfile(**_res['profile'])
                _res['role'] = role
            return _ret,_res
        else:
            # todo: auto generate new node name
            return False,{}
