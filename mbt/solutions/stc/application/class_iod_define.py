# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_iod_define.py
# ------------------------------------------------------------------------------
#
# File          : class_iod_define.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
# todo: here define IOD could be used in diagramCodeItem, but only OD writable.I only readonly.
# todo: diagram could directly use iod, (implementation in [userDefineCode,CodeFragment])
# todo: if use codeFragment the variables in fragment must also be referenced from IOD
# s1 = """
# xz=3
# xz+=1
# """
#
# s = """
# x==4
# """
#
#
# def util_is_py_statement(fragment: str):
#     _is_statement = False
#     try:
#         _code = compile(fragment, '<stdin>', 'eval')
#     except SyntaxError:
#         _is_statement = True
#     return _is_statement
#
#
# def util_execute_py_statement(fragment, context: dict):
#     try:
#         _code = compile(fragment, '<stdin>', 'exec')
#         exec(fragment, globals(), context)
#     except Exception as e:
#         print('util_execute_py_statement>', e)
#         pass
#
#
# def util_execute_py_expression(fragment, context: dict) -> any:
#     _result = None
#     try:
#         _code = compile(fragment, '<stdin>', 'eval')
#         _result = eval(fragment, globals(), context)
#     except Exception as e:
#         print('..>', e)
#         pass
#     return _result
#
#
# print(util_execute_py_expression(s, context={'x': 4}))
# s_ctx = {}
# print(util_execute_py_statement(s1, context=s_ctx))
# print(s_ctx)
