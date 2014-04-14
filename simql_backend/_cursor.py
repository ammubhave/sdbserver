class Cursor:
    def __init__(self, connection):
        self.description = ('name', 'type_code', None, None, None, None, None)
        self.rowcount = -1
        self.arraysize = 1
        self.connection = connection

    def callproc(self, procname):
        pass

    def close(self):
        pass

    def execute(self, operation, args=()):
        if operation == 'BEGIN':
            return ''
        #raise Exception('execute called _cursor: ' +  str(operation) + '\r\n'+str(args))
        import urllib2, urllib, json
        try:
            operation = operation.replace("%s", "'%s'")
            args = tuple([p.replace("'", "''") if type(p) is str else p for p in args])
            params = urllib.urlencode({'query': operation%args})
            #raise Exception(params)
            response = urllib2.urlopen(self.connection._database + "?" + params)
        except urllib2.HTTPError as e:
            raise Exception(e.read())
        self._data = json.loads(response.read())[0]
        for i in range(len(self._data)):
            self._data[i] = tuple(self._data[i])
        return self

    def executemany(self, operation, seq_of_parameters):
        raise Exception('executemany called _cursor: ' +  str(operation) + '\r\n'+str(args))
        return self

    def fetchone(self):
        r = self._data.pop(0)
        return r

    def fetchmany(self, size=1):
        r = self._data[:size]
        self._data = self._data[size:]
        #raise Exception(str(r) + str(size))
        return r

    def fetchall(self):
        r = self._data[:]
        self._data = []
        return r

    def nextset(self):
        raise Exception('nextset called _cursor')

    def setinputsizes(self, sizes):
        raise Exception('setinputsizes called _cursor')

    def setoutputsize(self, size):
        raise Exception('setoutputsize called _cursor')

    #    def execute(self, query, params=None):
    #    if params is None:
    #        return Database.Cursor.execute(self, query)
    #    query = self.convert_query(query)
    #    return Database.Cursor.execute(self, query, params)
    #
    #def executemany(self, query, param_list):
    #    query = self.convert_query(query)
    #    return Database.Cursor.executemany(self, query, param_list)
    #
    #def convert_query(self, query):
     #   return FORMAT_QMARK_REGEX.sub('?', query).replace('%%', '%')