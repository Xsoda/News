#*-*coding: utf-8*-*
__author__ = 'Xsoda'

import types
import re

isNumber = lambda x: type(x) is int

isString = lambda x: type(x) is str

isFloat = lambda x: type(x) is float

isDict = lambda x: type(x) is dict

isTuple = lambda x: type(x) is tuple

isList = lambda x: type(x) is list

isBoolean = lambda x: type(x) is bool
# 货币类型
isCurrency = lambda x: (isNumber(x) or isFloat(x)) and x > 0

isEmpty = lambda x: bool(len(x))

isNone = lambda x: type(x) is None

notEmpty = lambda x: False if isNone(x) or isEmpty(x) else True

isDate = lambda x: bool(re.match('\d{4}-\d{2}-\d{2}', x))

isEmail = lambda x: bool(re.match('[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$', x))
