# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : define.py
# ------------------------------------------------------------------------------
#
# File          : define.py
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
from wx.lib.embeddedimage import PyEmbeddedImage


class EnumBaseColour:
    COLOR_SUCCESS = '#99FF99'
    COLOR_ERROR = '#FF6666'
    COLOR_WARNING = '#FFFF99'
    COLOR_HIGHLIGHT_TEXT = '#333'


class EnumZViewFlag:
    REPARENT = 1 << 0
    DESTROY_ON_CLOSE = 1 << 1

if wx.Platform == '__WXMSW__':
    SCRIPT_EDITOR_FACES = {'times': 'Times New Roman',
                           'mono': 'Courier New',
                           'helv': 'Arial',
                           'other': 'Comic Sans MS',
                           'size': 10,
                           'size2': 8,
                           }
elif wx.Platform == '__WXMAC__':
    SCRIPT_EDITOR_FACES = {'times': 'Times New Roman',
                           'mono': 'Monaco',
                           'helv': 'Arial',
                           'other': 'Comic Sans MS',
                           'size': 12,
                           'size2': 10,
                           }
else:
    SCRIPT_EDITOR_FACES = {'times': 'Times',
                           'mono': 'Courier',
                           'helv': 'Helvetica',
                           'other': 'new century schoolbook',
                           'size': 12,
                           'size2': 10,
                           }

# Standard images for all the buttons we use in the dialog
# ----------------------------------------------------------------------
EI_CANCEL = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAABl0"
    "RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAQQSURBVHjaAEEAvv8BXTIyAAL9"
    "/UEy6Oip+fn5BqAAAHX1/f2bBP7+ACMDAwA4BQUAB/z8AAH6+hQhCQm7FAsLKpPm5qfh/f1g"
    "4QAAAAIAQQC+/wMtGBhBLufnr1w5ORI1JycI+traR9QBAev4/v7NFQICABsDAwAB/PwUFwAA"
    "vDdJSTA0X18DIujoL9Lm5iLZAACyAgBBAL7/A2ADA8xhKSkREoaGAAQ9PQAm398DAeDgRtP/"
    "/+gKAgLOHQEBDBr//782NDQwIGpqAP84OAAgFBQBKOXlLr3n5wcCAEEAvv8E9fn5CAcBAQD5"
    "3NwA+A8PAA5aWgBY+PgG/cjIlMcCAhUUAQFSMScnMB1VVQD/AAAA99HRAAj4+AAFBQUBAf//"
    "NAKI+TEf36uvT5546N+4wczMxcXwE2gYu6Qkg8T79yxCb986KUtKSiu7ujKwAA3/9ewZA/fN"
    "mwxX1q5lyD979sXZ//9LAAKImZeL69w5oJ//v37tqvP4MQsj0IA/wEBjBWrg+fmTUVRZmYGD"
    "lxesmePpU4Zbx44xFF269OLQ379xQAftBgggZgFOToYvf/+ePcPA8ILl0yc35RcvWP79+sXA"
    "9PMnAxc3NwML0LA/L14w/H79muHarVsM5TduvDj6928UUPNeIGYACCBmbXFxBkFgVPEwM597"
    "xcn5W/DXLxexp08Zf338yPDn/XuGX0CNPz5/ZvgGNLD93r13R37/DhBkYDjMA9QMChOAAGLR"
    "FBEBpQOG/3/+8Mn+/Bmi8OkT40eg5ncfPjB8BXqHhZ2dgRvoHVFRUQYvMTHuN48fa/xgYDjG"
    "C9R8H4gBAohZDxhgP///55H68eOg34sXxmJAze+BEh/+/2f4DqT/sLAwsAK9ycbGxmAhJcUi"
    "yczscfrDh9dAQ85+BcoDBBCztoyMpMz37/vCnjwxkAY69QNQ8BsQswI18EtIMHACaRBgBbqE"
    "CYiNZGRYRP//d738/v3rF0BDAAKI2U9A4EjMw4f6il+/MnwEKvwJxCBNT4SFGab/+PGem42N"
    "WY+bm/kvMFWyAMWZga4xVVBgkfj3z23f27cPAQKISebzZ21toOa/QI3/gJgfGKCPgZq7v317"
    "sfPdO7+Fr19nnv/585cIUCMTKMEBY4UFmF7M5eTYBJmZkwACiPk1F5cCPyengTYwzlmBtpwG"
    "aq7//v3F+Y8fo9gYGQ+xMzCcv/7ly0sxFhY3HSEhFkFgmvgEjJ2ms2d/7Pz6dSpAADHIAkNX"
    "R1x80SoxsX+bxMX/6/HzPwc6xBnkbw6gjWpAF6kDaUNGxoxFSko/7lpY/E/n5//ByMBQAlID"
    "EEAMqmJiDNJAWxX4+dsluLh2A8XcGKAAZoA+MEdqAvn6jIwx+iwse5kZGAphagACDAAeLHBa"
    "S9SUbwAAAABJRU5ErkJggg==")

# ----------------------------------------------------------------------
EI_CLEAR = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAA"
    "B3RJTUUH1wYeFCULmGdR+AAAAnpJREFUOI2V0ktIVFEcBvDv3jveufO4jk46ZVlGNUGRLTIp"
    "K8OCoAdBIM2ioo2LCKFsI7QJCQoiiJ60nCDBTbUpsJSh0cxw42DImA2j1vhImXFmvPM493VO"
    "izDS6WFn/X0/+H8cDv/xHpyzXuYs/FVdVT2iVbre/CTXxq+0fP+M9ZLNId/YVd+4+tTZFo5o"
    "rBUAVgQ8PI9VsOBmTf1JR3+wE18igyCcHAUAy0oAysSLFeuqBJFMoW7nerwZ+JzLGFLLP4FP"
    "70r7KOOeBzqMZpeYl+KxEPqiYlbVhHt3XnwN/PUEf5tfMg3Lfrmk+tYhn3VNWXUeUYXXFogQ"
    "GhNi1xZzwp+AxiN7H01EjtaoxCt4KmvhLMvA6priqzaTjrxFDQSDYADALS+Ov4WkWzxPDWY7"
    "np4/IY0Ob+RHQgrc5QnsafgIQx+CrqH1WJNyuwCI9DrLqeAI2GXvlrVVp22MmdDyMYyPJvDM"
    "TxEJ21HXMNBeXjvU5PNBWwJEu0tdpk18L5ft9pa4a0ShSIapzUGZHwEvZKCTafR2ZzXOmfP4"
    "LiTTiz0eAGL9lTbDLnY53dWbZNd2MZuegKnHoeYnkVuIQVdnoKszcDhTBVvxAJCj2iuH7N3h"
    "kLfapsdewlFcAY1MITU7AmokoaSmAVDoKoDkbwBK1cOi6LZPjLbD6fJCV2cQDfeAZGdBzSSS"
    "CQrGAMPgeJBkvgAAuIZvk0HoGiBKEsKhTj0VT4IaC+AFA/E5DprKATzSvrYf4y0Bth1M9RDT"
    "soHSosfhwdcsq5AiajBqmgbyhEdGARJxRnmOdS/foOAfAECXv9hrmuwuIeyApqL4Z5jn9vmu"
    "KB9+zX4H1k8cy/juDWsAAAAASUVORK5CYII=")

# ----------------------------------------------------------------------
EI_DEFAULT = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlw"
    "SFlzAAAK8AAACvABQqw0mAAAACV0RVh0U29mdHdhcmUATWFjcm9tZWRpYSBGaXJld29ya3Mg"
    "TVggMjAwNId2rM8AAAAWdEVYdENyZWF0aW9uIFRpbWUAMDIvMTEvMDeS+i0/AAACvklEQVR4"
    "nKWSXUjVdxjHP7/f/+W8qdPqj5rRPAsryDM2FIRBjEQotjuHsV2NCIPqoqju6iqnuYu9ZKtw"
    "N7mKujGqDXQ3o9UQEsl8mYl1OGp5lDRt5+h5+Z/j///rIgVfops98MDDw/N8+D4vQinF/zG5"
    "NtHU2LDn8qWL1StS1q329khj43dPZ1/P578X8Mfvdw/W1Oy9Mzo21l5bW1vjy/XKCy0tZ4LB"
    "YHBudq6s/uC3x9YCdADchIUMzHR13du/9cOyvEgkAspp7uvpMzs7/wz9dP5nno2GldBFIWAA"
    "2dUKhMoODju1wZ11u65fu0o0GnW2lIbse38/CMXiMR739rF722fcbrr5iZ1JhFYqEG+XOCR+"
    "aStr/W/erNfFDAG/oYpzXtrXrh7x9j4b52T5VxyvPMHAZA+bzlZt3Fxgza0egV0qmcy+TsRB"
    "ahYTzxFf11327jtXxmSsku0l20hfuE9qmnSgwFp1tqUl9oFAahKkAE1X2Il5csxpthdPwNg/"
    "QAqh68IF8Q5AaY6hu7arKaQXhAZCGiB1cAS4BkJqCEN6AmQ3rb8CnhJpZ/qHHjrkF9r4/Dmg"
    "ZcFYAkhBMp3GNfMepTHC5nqAb2TqZWJrMu4wM5lkYTHKSO4gRVUpKC1CMwMMd00ytUNMV4H7"
    "DgWQXURJAZqhkcnAq5EIsdlpjKJxuiMbyA7v58nGoY/vHD5QveWDwti55ubHgLv8SNLjdV3d"
    "cFhcANcRxFIJpN+DtpDgxWiaT/MsOu9fKentCv+lS42Ojo6m/oGB08uv/NGhA/qjyqr5b8pD"
    "dnd+QZxcv4lKJzGERkxPcjLRwr/OKHbaxvR4lGVZDwFQSi15dDk2w2MTX6Qe/Ppj+PsvpzIN"
    "5W5zdZ5Cw/X5fcmKiorrbW2/7VjuWwFY73GlyrP9N9pbT9WNf16z94emxoaja2veALFzTWMO"
    "z/GRAAAAAElFTkSuQmCC")

# ----------------------------------------------------------------------
EI_HELP = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAC+ElEQVR4nGWTP2xbVRjFf9+9"
    "9/01TgwJCQkMbkMKqCkEKGoXBpiQEqkpZUL8y8BeRqYwMMBQRMWMGtQgJCSKYWCohARIVCCo"
    "MJUgLbSipVERTuzYcexn+713L4OlirafdLZzznC+c4TbbnZxrSTIEkoeQ9S8iICob0WkevHM"
    "C5Xb+XKLeOH08WIxXnloZqoUhSFRFDHIcmr1XerNDts7navWuTfWPz1SucNgduH0qfm58mt7"
    "y/ezfq1LrZmR2SHFaAg9QTtLo1WnnybLv3+yuHrTYHZh7a1DT8ysFEfH+eVyh73TEa8vTvL0"
    "o0WsdXzz6w6nzm5x5cYALdDtNMgG3aO/ffxcRWYX18pTE6W/Dj7+CN9daDM17lN5+2GsteS5"
    "w1qLc44b9ZSXTlxHRHDOkrRqTWvzPXp837GVw0/OHl7fyOiljt2eJQ4U9VbGiTM1HLBn0iP2"
    "hR8v92n1QGmNaB3m6eCS8QNvSZmI7XYXRECED76skTshs6C18OyBGOccm7uOTjrMLNQRottH"
    "zOhIoVxrpsM0BPqpo9vJEa15YMLnzWNjWGs590efRg/8yABQUJB0dclYB71BjnWwvZORI3i+"
    "RnuKd16ZIA6EK/9mnPy6QxB7KDV8XDFw1BsGM0hzBMfmdooTwfgKZRQLB+9iZtJgrePD7xNS"
    "ZQgChdIKgJGCRZRGdZJBpd1OsM4hSlB6iKl7DM45nHNc2nQEoSGIPMLYY2TEIwxAtKkaRH3R"
    "au8uFcNRulZQaojKzwn7pn22EjC+xgs0fuhhfE15DP5cbyFKf6Qufvb8atJPqpHOMQKIIEo4"
    "+lTMoRmfhTmfuWmD9jReqJm+10ORs/FPv3L+/QNVBeBwy4O01QzE3uz2hesp3QFs7MDfTYdR"
    "cN+oUPIyzv3QqIrSy7dsYf+LX82jzOe5GS3rsEgcGeKCR6FouLvkMVYybDV6XNtIqoNMnvnp"
    "3Qebd6xx7uWzJZQ6Ltp71XhBOS7EhJEhzS27SV4VbU6ef2//6v81/wH6bjI8fK9HXAAAAABJ"
    "RU5ErkJggg==")

# ----------------------------------------------------------------------
EI_INFO = PyEmbeddedImage(
    "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")

# ----------------------------------------------------------------------
EI_OK = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAANkE3LLaAgAAAjpJ"
    "REFUeJy90k1IkwEcx/Hvs2evMt1KJ741Wy0zexMy0US6WHSKgii8pAUZKUEFubSgkjKRQgT1"
    "kL0hZNChMpJCi/RQGQll0sBE09wWw5c2c5rbs+fptIgutQ59758//8MP/nNCcsWSm5ajS+8C"
    "6qh1con5So+3W3ni6lTiS81XAe1f45QDsXV3JloVT2BC8c57lGZng6LZJVz8+Ub8fpVD0Mri"
    "1DVqf8dpZYYLZ6pOOjJi1jDqHyIoS7xwdyMbla1qANNO7fHDx0rrZPV3WufbpOl26iM4/Yju"
    "XEXlwdNWvZ3xuY9IssKDT23c6+0l3McjUVfEoe2Vm5vyEwuJ1yVgyRO3jflHfIFBXtvK1dUl"
    "jt016ZpM/MFJZiUfTyfbed7/Ct9t6hmiRkzeR2Moddo6G5xBJYZJjEkiMUcoIvtrzo7iLeUp"
    "Ohu+oJcpycPA3DPefXiP6zoN0gAOQBYRyLRslAqmtS7coSF8iguNQVFZs0yrtYIGb2iE0eBb"
    "3OFBvMMzOBuk2oV+qgAZQFz8zMvwPGkrc3XZQlyIb4KfsNqPUYhFL6pRqWQMOjULEwJ9l3yX"
    "Z/uojmAAEQgFhukKLsq2rLyE9XqTiiTtMuwxWaQb7Cw3ZjDjCtBx1tk41SNX/oojBwBCfidd"
    "QUlalVtgX5tqsmHVrWCdKZfxL2M0nXrY4nksnQDCf9pL3IZy/f1m917ljXxD6fCeV+zF2ugW"
    "B5gLHcbOFtceZVOZ4RagjwZHSrLkUwHE/guOqh90ld9+870vDgAAAABJRU5ErkJggg==")

# ----------------------------------------------------------------------
EI_REASSIGN = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAGXRFWHRTb2Z0d2FyZQBBZG9i"
    "ZSBJbWFnZVJlYWR5ccllPAAAAsZJREFUeNqck1lIVGEUx393thaXCm0qtdJrm4FlONGkWESb"
    "tthDUA9F9dDyFhTRghI9WJpgPgSBD/UWQRvZrg6CSFk5FuJDD+nYTFCmmaDV2Cz3dr7LBEIv"
    "0oE/937nfP/DOed/Pm1XPZMyU2AYNBom5TYNzWYDTXw2KyhRCVjff4iJWDwOv2OU1+5tYDyK"
    "qc7qui1u8EACpnJGYtyVsxVQUP8Zs3QzHMH8JfDq0Nl3jIrycyqZKRWhldZiXt1XQSQeo6PP"
    "j/9jP6HhgKbKm5+mmx5dx5tbKFVoAged/VXYpe7Zyfu45ruJQ93sDF4kHAXvovOkp6zmec9t"
    "q5kdBfvJmeugI3AeK6Mq2SGQBCPhkHW2L97IoXchZqYmwc9oG0vmFZAydSHBbwE2r9LpDF0i"
    "OAhdfeAUonuWkH/o3HvVTdNpPPZeH74+Hzdc+ZTNSGbGOG/IdS9jqtPNrVfXZdzwoptg40k2"
    "TVnF0bSZTlreDtN8Bk95PV12kXFo6Va+PDtDiy2fw0nTscftPeS4c0hx5fL4dW+ktZL1O+vo"
    "joYpDQ4ZWU2KfIUu1ZZNNdt4wmRzNfcPbNzuGh7RCQxA/+gTFmT8ZE9JkUtidx6elJtOvHUH"
    "G9hUjf+vWjYjTuuWGs3cXVK8OCtzjOKiAP2SIPgVPofbUb7t3uV5G6o0c+1KGfiQyLhHZIwm"
    "ZCy7jHn8QB7x2DSGwm8JfYIvId2a8NzMANlZkOpaRMwYs6Qc+z2AbCJuh8j4SGRU+zhivCcm"
    "9QQ/w8sOBpsrA9tUgi0XeSJDnKNn92IkFktLyPg9IaNWWoVfc1GoVjYe5nXLBY7IYHuwZkN+"
    "WQ2twktX5OI1IHvFyIDO07YAzWfxqPVYIkhJrP6okD9MfAuSZAVqfGLSrn9diYu29gjPEzJq"
    "k32NysZHaXUmseHxKTzC6+I/LFdQONHxR4ABANuzKntCBWfVAAAAAElFTkSuQmCC")

# ----------------------------------------------------------------------

EI_HTML_BACK = PyEmbeddedImage(
    "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")

# ----------------------------------------------------------------------
EI_HTML_FORWARD = PyEmbeddedImage(
    "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"
    "AAgwANtDcqAqYx6xAAAAAElFTkSuQmCC")

# ----------------------------------------------------------------------
EI_HTML_HOME = PyEmbeddedImage(
    "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")

# ----------------------------------------------------------------------
EI_HTML_PRINT = PyEmbeddedImage(
    "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"
    "rkJggg==")

# ----------------------------------------------------------------------
EI_HTML_RELOAD = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABGdBTUEAAK/INwWK6QAAABl0"
    "RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAlZSURBVHjabIvBCYBAEAOT027t"
    "xI/VWJA/i9DkonsfwYEhw8LSNh64EP/kroxbZKnRXzaIJ+62QpMj0qVm4BqN+vN+vNsFEBMD"
    "JeAfIxJm0mf486+D4fvXtUDjlYg1AiCAKHMAAzRkQCH048evONtYhjiHpECGL5+PMPz9E0uM"
    "doAAotwBoCD9Dwzi3//+KosoMizMmsswMXWWJAcjywKGH1/7GRgZ2fDpBgggFiJtEWH4/0+T"
    "4c9/VYa/DNxAH/9j+A+NAnAIMP5m+MGg+PP7b4ZPjI8YorztGcyV9zPFTUwquPXgqjYDpzAo"
    "NF5iMxgggPA74B+DIsOv//lA2pWHm19dVliWmZuVFxLksDTwH5IGfnz7yaAkpMrwluE5w+rf"
    "3Qx+GvkMB1t3MoS2x7oeuXhoIwOnYABQxwt0KwACiBFrLmBkYGP4zVAG9G2lm7YHV5ZtNoOJ"
    "ihEDOycjw1+gZ7EmBSBkYmRiuPLnGMPen4vBhrjxRTDof/dlCG6KZ9h3Zu8JBk4hL4b//98j"
    "5wKAAMLmAE5gcM6SEZKNmRE1g8FOz4rh1I+dDBe+H2X48Oc1w+//v8HW4UoPf///Abr7L1jN"
    "9/9fGOx4fBkcGWIYvCtjGM7dvtLEwMpeD3bAtgdgHQABhB4FzECfz1cSVw7fmbOT4R3/Q4by"
    "h9EMH36/ZvgHdOgfIMRpNxSwMXEwcDJxgh3z5e83hqM/DjIEKqczaMnpMJy7ekGFgZkdRT1A"
    "ALGgpOY//yNFOEXC1yavY7jOcpJhyo1WBmYmFoZ///4yyHEqMejxmjKIsUowIBIBamb4++c/"
    "w9XPFxkufjnF8PPvdwZpDjmGasVJDDNXrmJYtnP5FwZOnuno2gACCDkEhIG+r2sMbGZgFfzL"
    "0H6lloEJaCoT41+GLPlSBjtOL4aL964xPP/wAiQKDQlotAET4u8/vxksFSwYuPgEGFY9XcLg"
    "IOTO0KE4nWHx+i0MBTMrfwB9ngRUfwTdAQABhHDAn/+eEgISKt46XgzVN/MY3n79DLagQbWD"
    "QeOLKUPA9BCG03dPvmD48/cOpChmYmT4zwwJjH+M/xi+/NApiqgTNPVUZPAWDmcolW5iaF8w"
    "k6Fn9cQvDGzc6QxMzKvh8fcXUfwABBDCAT8ZnJ11XRjv/r7FsPHhNnBiC5EOYTD4Z83gPNGZ"
    "4fnrJwsZOHiLGZj+v4XEAFLZDqLZmbf/Yfzj4SsWyKD5w5QhuauEYceJbfcZOAXSgJbvAVv+"
    "H6r2H8IBAAHEgpSPdC0VrRh+/vnBYM1nDwx6ZoZs+QKGlYdWgCw/DgzbFKBlwFQITOEsQIN+"
    "MUJiAGTYP1aQFCMLIwvD5qP7GQpm1TK8fPV8MwOPcDYw2z0GBxO0vEAHAAGEcAAjo8zjj08Y"
    "lN+pMOTwFUFS8YtfDLtu7AN6lnUHMMj/MDACfcH6H2IQB9DQ30DLv3BCkz8Pw9KDmxj61899"
    "9x9UKXHzdTMw/0ZY/B97bQsQQIhyIIX9HPM/JgWmf8C8BilewcXsn79MHMAipgxo+QwG1t+Q"
    "sP/HJAmknwHd+J/hnQDMqD0Mv/7yMTCxZDAw/z/HwAgOZ05oGoGGFDzt/Pm/7+YPkC6AAEKK"
    "Akbrv//+s/wFlfL//kPSC4gGBg0Qf2dg/gsKFHGGv//6gW6QBXJswWoQPstiYGZ5BqS/AC0H"
    "qfUEql3I8P3nH6DF/+AOYGRhYWDjBEYLgzFIE0AAIWfD7wzAohQY+ZAE9h9KM/+BZrdfnkDD"
    "enl4xDS//vh5CF4egYIZ1OD4z3QLGqYQ9b9+i8iLyQpPymoHFkxcDKCAZmT5z3DuzlWG6um9"
    "8FQIEEAsOCIGgln+gAKAi+H79zo2Zo6y1th+RkYmVoaS2YXAtMABzLrAUg3kW2DyAAczI6zV"
    "BMyeXz/aOmpaM/hZ2jLs+r8EmKt+MFgyuTLwsFsy/P3x+z3MKoAAwu4AJnhJJ8vw5dscdUkt"
    "txlpsxgctK0ZZu5ZALQYGDdAh4DTCpZqieHbl2wuTv7oLP8UhgM/NzCsfjMLWEf8Y1CSNmA4"
    "fvEeMMv/fghTDRBACAdgtPP+mzJ8/rHE2yxAbWHmfIbLrPsYzv/Zz/DvF1Dq818tBo4vK4EO"
    "YIImLFhC+wesLpWlhaWNJxX0M0hrsDO0PpnH8O8vG4MIsAiX/KfOsGrvJGC0sR+F2QIQQMiJ"
    "EMnu/7oM335sjHVMlpyWOoFh7ceZDCsfzmQok+9mcFJ3YKiObxJlYeEIgzdSofgfMAUrSioy"
    "2BuZMfwWec3QfC8fWIN+ZPjx7ztDnFQRw8njtxlOXzz3CVivr4dZBRBALFgqFRlgsbo2zS1H"
    "sj+xg6H3cSXD4Xe7gbUcJ8OpV8cZbIR4GHxDbRDBjRxzwDTw5tdzhoUfWxkuXD3NAMrRP//+"
    "ZPCTiGAw+uPBYD01AlixMcwFqrwA0wMQQIhyIIEbmnq/TzZTss7ZUbWBofF+PsPJD4cZ+FkE"
    "wHI/gT75+e8HohLC2iz5D66sQJAFWJNGyCQwRAvmMcTXljOs37vjFAM3jwsoEv8fh7gBIIBQ"
    "0wBE6P3nr58Yvn76ziDAIAoMjO/AopwdmBmAQQxMSH+BDVBGfI1MYOLkZeZlMBI0ZYiWTmb4"
    "85yXwb02leH4aaCNvPwRQPd9RlYPEECYaYCZo/v6g8v2CdMz7JZlzGNg+cfJMPfRVHC7IEIs"
    "nsFbJJDhN7BZxoie8oEiIEeyMbIz8PzjY/j0+hfD9BnbGZZuW8vw/hMwwfIKFADVYbQJAQII"
    "Mw38//+ZgZM/fO+5HVsDeiKMFqbPYhCWF2WoulHKIMEqxfD25k+GCVumMrCxciP1lBghDgDm"
    "hu8/fzM8ev2S4f7zp+//fft6Bljq9TNwcG7H1ZQCCCBEGojlQ3gG3K1ilWP4/HmBhqyu4+zE"
    "KQyP+W4Cs/9vhoenPjPUzqp4zMDOuwiRDZlhPSQmIPsHAxPbQ2A5cRqY2K6gFdcIf56ApAGA"
    "AMLdLP///xEwJLxuPL7V59YWlNkUWs2Q7h7JMIV1CbDu573LwMFdA7EYuRxgRLDBFv/Hk2Ah"
    "ACCACHRMgOUnO0/W91//LpTOr2k9//CKiCCPENBMViZwwxdc7v9Hy46ELUUGAAFERM8IaCAz"
    "yywGDpbDy3avncjIyuXKwMrFimEvmQAggIjsmoFsYrrOwMHl/f8vcyWwWaUI9SbFTgAIMAAF"
    "XnDxjsZXyQAAAABJRU5ErkJggg==")
