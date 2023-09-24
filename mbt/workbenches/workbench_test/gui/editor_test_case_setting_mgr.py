# -*- coding: utf-8 -*-
import wx

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : editor_test_case_setting_mgr.py
# ------------------------------------------------------------------------------
#
# File          : editor_test_case_setting_mgr.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import addict
from framework.application.define import _
from framework.gui.base import FeedbackDialogs
from mbt.application.project import EnumProjectItemRole
from mbt.application.base import MBTViewManager, MBTContentContainer
from mbt.gui.base import MBTUniView
from mbt.application.workbench_base import MBTBaseWorkbenchViewManager, MBTProjectOrientedWorkbench
from mbt.application.define import EnumAppSignal, DF_PY_OBJ_FMT, EVT_APP_TOP_MENU
from .editor_test_case_setting_cc import TestCaseSettingContentContainer, SettingPropertiesContent
from .editor_test_case_setting_view import TestCaseSettingEditorView


class TestCaseSettingEditorException(Exception): pass


class TestCaseSettingEditorManager(MBTViewManager):
    def __init__(self, **kwargs):
        MBTViewManager.__init__(self, **kwargs)
        self._needToSaveElNames = dict()
        # todo: receive node delete or reprofile event, update this cc.m_bind

    @property
    def workbench(self) -> MBTProjectOrientedWorkbench:
        _f = [x for x in self.ancestors if isinstance(x, MBTBaseWorkbenchViewManager)]
        if _f:
            _wb_vm = _f[0]
            return _wb_vm.workbench

    def get_bind_model_node(self):
        _bind_model = self._contentContainer.get('m_bind')
        _bind_uid = _bind_model.data.bindUid
        if _bind_uid is not None:
            return self.workbench.project.find(self.workbench.project.projectTreeRoot, lambda x: x.uuid == _bind_uid)

    def create_view(self, **kwargs) -> TestCaseSettingEditorView:
        if self._view is not None:
            return self._view
        _cc = TestCaseSettingContentContainer()
        self.post_content_container(_cc)
        # call cc.prepare(), load all necessary data (query) from content provider. if None then insert new one. store in a dict
        _cc.prepare()
        _view = TestCaseSettingEditorView(**kwargs, manager=self)
        self.post_view(_view)
        _bind_info = self.verify_bind_model()
        _view.render_form(bind_info=_bind_info)
        _view.Bind(EVT_APP_TOP_MENU, self.on_top_menu)
        # EnumAppSignal.sigSupportedOperationChanged.send(self, op=self.get_node_sop(_node))
        return _view

    def verify_bind_model(self):
        _bind_info = dict()
        _node = self.get_bind_model_node()
        if _node is not None:
            _bind_info.update({'name': _node.label, 'path': _node.get_path_string()})
        return _bind_info

    def do_sop(self, sop_id, **kwargs):
        """
        execute supported operation (copy,cut,paste currently)
        Args:
            sop_id:
            **kwargs:

        Returns: None

        """
        _item = self._view.treeView.GetSelection()
        if not _item.IsOk():
            return
        _node = self._view.treeView.item_to_node(_item)
        if sop_id == wx.ID_COPY:
            self.copy_node(_node)
        elif sop_id == wx.ID_CUT:
            self.cut_node(_node)
        elif sop_id == wx.ID_PASTE:
            self.paste_on_node(_node)

    def notify_bind_prototype_required(self):
        _cc_c=self._contentContainer.get('m_bind').data
        _already_bind_uid = _cc_c.bindUid

        def filter_(node):
            return node.role == EnumProjectItemRole.PROTOTYPE.value

        _selected = self.root.choose_project_node(filter_,[_already_bind_uid])
        if _selected:
            _selected = _selected[0]
            if _already_bind_uid is not None:
                _ret=FeedbackDialogs.show_yes_no_dialog(_('Rebind'),_('Rebind could cause the setting data reset! are you sure?'))
                if not _ret:
                    return
            _cc_c.bindUid=_selected.uid
            # todo: bind version???
            # todo: analyse the model, generate the baseline data.
            self._view.render_form('outline',bind_info=self.verify_bind_model())

    def notify_content_be_edited(self, which: str):
        if not self._contentContainer.has(which):
            return
        self._needToSaveElNames.update({which: True})

    def notify_content_restore_required(self, which: str):
        if not self._contentContainer.has(which):
            return
        self._contentContainer.reset_to_default(which)
        self._view.render_form(which)

    # --------------------------------------------------------------
    # event handling
    # --------------------------------------------------------------
    def on_top_menu(self, evt: wx.MenuEvent):
        _id = evt.GetId()
        if _id == wx.ID_SAVE:
            _ret = True
            _success = []
            self.root.set_status_text(_('start saving %s content...') % self.viewTitle)
            for k, v in self._needToSaveElNames.items():
                _ret &= self._contentContainer.change_apply(k)
                if _ret:
                    _success.append(k)
            [self._needToSaveElNames.pop(x) for x in _success]
            assert _ret, TestCaseSettingEditorException('follow content not successful saved.\n%s' % '\n'.join(self._needToSaveElNames.keys()))
            self.root.set_status_text(_('saving %s content successfully processed.') % self.viewTitle)
