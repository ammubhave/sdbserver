from _simql_exceptions import *
from _connection import Connection
from _cursor import Cursor

apilevel = "2.0"
threadsafety = "0"
paramstyle = "format"

#Constructors


def connect(database):
    return Connection(database)


def register_converter(typename, callable):
    pass


def register_adapter(type, callable):
    pass
