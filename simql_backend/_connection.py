from _cursor import Cursor


class Connection:
    def __init__(self, database):
        #raise Exception('__init__ called, _connection')
        self._cursor = Cursor(self)
        self._database = database

    def close(self):
        #raise Exception('close called, _connection')
        pass

    def commit(self):
        raise Exception('commit called, _connection')
        pass

    def rollback(self):
        #raise Exception('rollback called, _connection')
        pass

    def cursor(self):
        #raise Exception('cursor called, _connection')
        return self._cursor
