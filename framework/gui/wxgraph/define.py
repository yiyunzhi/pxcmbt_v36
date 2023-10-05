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
DEFAULT_ME_OFFSET = 5

IDENTITY_ALL = 'ALL'

BASE_SHAPE_DOCK_POINT = -3


class EnumHandleType:
    LEFT_TOP = 0
    TOP = 1
    RIGHT_TOP = 2
    RIGHT = 3
    RIGHT_BOTTOM = 4
    BOTTOM = 5
    LEFT_BOTTOM = 6
    LEFT = 7
    LINE_CTRL = 8
    LINE_START = 9
    LINE_END = 10
    UNDEF = -1


class EnumShapeSearchMode:
    UNSELECTED = 0
    SELECTED = 1
    BOTH = 2


class EnumShapeTreeSearchMode:
    DFS = 0
    BFS = 1


class EnumConnectionPointType:
    TOP_LEFT = 0
    TOP_MIDDLE = 1
    TOP_RIGHT = 2
    CENTER_LEFT = 3
    CENTER_MIDDLE = 4
    CENTER_RIGHT = 5
    BOTTOM_LEFT = 6
    BOTTOM_MIDDLE = 7
    BOTTOM_RIGHT = 8
    CUSTOM = 255
    UNDEF = -1


class EnumShapeConnectionSearchMode:
    # Search for connection starting in examined shape
    STARTING = 0
    # Search for connection ending in examined shape
    ENDING = 1
    # Search for both starting and ending connections
    BOTH = 2


class EnumShapeBBCalculationFlag:
    SELF = 1
    CHILDREN = 2
    CONNECTIONS = 4
    SHADOW = 8
    ALL = 15


class EnumShapeHAlign:
    NONE = -1
    LEFT = 0
    CENTER = 1
    RIGHT = 2
    EXPAND = 3
    LINE_START = 4
    LINE_END = 5


class EnumShapeVAlign:
    NONE = -1
    TOP = 0
    MIDDLE = 1
    BOTTOM = 2
    EXPAND = 3
    LINE_START = 4
    LINE_END = 5


class EnumShapeStyleFlags:
    # Interactive parent change is allowed
    REPARENT = 1 << 0
    # Interactive position change is allowed
    REPOSITION = 1 << 1
    # Interactive size change is allowed
    RESIZE = 1 << 2
    # Shape is highlighted at mouse hovering
    HOVERING = 1 << 3
    # Shape is highlighted at mouse select
    SELECTION = 1 << 4
    # Shape is highlighted at shape dragging
    HIGHLIGHTING = 1 << 5
    # Shape is always inside its parent
    ALWAYS_INSIDE = 1 << 6
    # User data is destroyed at the shape deletion
    DELETE_USER_DATA = 1 << 7
    # The DEL key is processed by the shape (not by the shape canvas)
    PROCESS_K_DEL = 1 << 8
    # Show handles if the shape is selected
    SHOW_HANDLES = 1 << 9
    # Show shadow under the shape
    SHOW_SHADOW = 1 << 10
    # Show connection point on the shape
    SHOW_CONNECTION_PTS = 1 << 11
    # Lock children relative position if the parent is resized
    LOCK_CHILDREN = 1 << 20
    # Emit events (catchable in shape canvas)
    EMIT_EVENTS = 1 << 21
    # Propagate mouse dragging event to parent shape
    PROPAGATE_DRAGGING = 1 << 22
    # Propagate selection to parent shape
    # (it means this shape cannot be selected because its focus is redirected to its parent shape)
    PROPAGATE_SELECTION = 1 << 23
    # Propagate interactive connection request to parent shape
    # (it means this shape cannot be connected interactively because this feature is redirected to its parent shape)
    PROPAGATE_INTERACTIVE_CONNECTION = 1 << 24
    # Do no resize the shape to fit its children automatically
    NO_FIT_TO_CHILDREN = 1 << 25
    # Do no resize the shape to fit its children automatically
    PROPAGATE_HOVERING = 1 << 26
    # Propagate hovering to parent
    PROPAGATE_HIGHLIGHTING = 1 << 27
    # if ration keeping while resizing
    RESIZE_KEEP_RATIO = 1 << 28
    # if fixed the center of the shape while resizing
    USE_CENTER_RESIZING = 1 << 29
    # if disappeared while too small
    DISAPPEAR_WHEN_SMALL = 1 << 30
    # if set the alignment allows not be processed.
    DISABLE_DO_ALIGNMENT = 1 << 31

    STYLE_DEFAULT = (REPARENT | REPOSITION | RESIZE | HOVERING | SELECTION
                     | HIGHLIGHTING | SHOW_HANDLES | ALWAYS_INSIDE | DELETE_USER_DATA)


class EnumGraphViewWorkingState:
    READY = 0
    HANDLE_MOVE = 1
    MULTIHANDLEMOVE = 2
    SHAPEMOVE = 3
    MULTISELECTION = 4
    CREATECONNECTION = 5
    DND = 6


# class EnumShapeSearchMode:
#     SELECTED = 0
#     UNSELECTED = 1
#     BOTH = 2
class EnumDrawObjectState:
    NORMAL = 0
    HOVERED = 1
    HIGHLIGHTED = 2
    SHADOWED = 3
    SELECTED = 4


class EnumVAlignFunction:
    NONE = 0
    TOP = 1
    MIDDLE = 2
    BOTTOM = 3


class EnumHAlignFunction:
    NONE = 0
    LEFT = 1
    CENTER = 2
    RIGHT = 3


class EnumSelectionMode:
    NORMAL = 0
    ADD = 1
    REMOVE = 2


class EnumGraphViewStyleFlag:
    MULTI_SELECTION = 1 << 0
    MULTI_SIZE_CHANGE = 1 << 1
    GRID_SHOW = 1 << 2
    GRID_USE = 1 << 3
    DND = 1 << 4
    UNDOREDO = 1 << 5
    CLIPBOARD = 1 << 6
    HOVERING = 1 << 7
    HIGHLIGHTING = 1 << 8
    GRADIENT_BACKGROUND = 1 << 9
    PRINT_BACKGROUND = 1 << 10
    PROCESS_MOUSEWHEEL = 1 << 11
    DEFAULT = MULTI_SELECTION | MULTI_SIZE_CHANGE | DND | UNDOREDO | CLIPBOARD | HOVERING | HIGHLIGHTING


class EnumShapeShadowMode:
    TOP_MOST = 0
    ALL = 1


class EnumPrintMode:
    FIT_TO_PAPER = 0
    FIT_TO_PAGE = 1
    FIT_TO_MARGIN = 2
    MAP_TO_PAPER = 3
    MAP_TO_PAGE = 4
    MAP_TO_MARGIN = 5
    MAP_TO_DEVICE = 6


class EnumConnectionFinishedState:
    OK = 0
    FAILED_CANCELED = 1
    FAILED_AND_CONTINUE_EDIT = 2


GV_DAT_FORMAT_ID = 'ShapeFrameworkDataFormat1_0'
