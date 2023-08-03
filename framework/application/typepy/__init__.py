"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from .__version__ import __author__, __copyright__, __email__, __license__, __version__
from ._const import ParamKey, StrictLevel
from ._function import (
    extract_typepy_from_dtype,
    is_empty_sequence,
    is_hex,
    is_not_empty_sequence,
    is_not_null_string,
    is_null_string,
)
from ._typecode import Typecode
from .error import TypeConversionError
from .type import (
    Binary,
    Bool,
    Bytes,
    DateTime,
    Dictionary,
    Infinity,
    Integer,
    IpAddress,
    List,
    Nan,
    NoneType,
    NullString,
    RealNumber,
    String,
)

__all__ = (
    "ParamKey",
    "StrictLevel",
    "Typecode",
    "TypeConversionError",
    "Binary",
    "Bool",
    "Bytes",
    "DateTime",
    "Dictionary",
    "Infinity",
    "Integer",
    "IpAddress",
    "List",
    "Nan",
    "NoneType",
    "NullString",
    "RealNumber",
    "String",
    "extract_typepy_from_dtype",
    "is_empty_sequence",
    "is_hex",
    "is_not_empty_sequence",
    "is_not_null_string",
    "is_null_string",
)


def get_type_cls_by_type_code(type_code: Typecode):
    if type_code == Typecode.NAN:
        return Nan
    elif type_code == Typecode.NONE:
        return NoneType
    elif type_code == Typecode.BOOL:
        return Bool
    elif type_code == Typecode.BYTES:
        return Bytes
    elif type_code == Typecode.DATETIME:
        return DateTime
    elif type_code == Typecode.DICTIONARY:
        return Dictionary
    elif type_code == Typecode.INFINITY:
        return Infinity
    elif type_code == Typecode.INTEGER:
        return Integer
    elif type_code == Typecode.IP_ADDRESS:
        return IpAddress
    elif type_code == Typecode.LIST:
        return List
    elif type_code == Typecode.NULL_STRING:
        return NullString
    elif type_code == Typecode.REAL_NUMBER:
        return RealNumber
    else:
        return String
