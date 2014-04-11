import simql.query_handler


def check_strong_read_on_columns(table, columns, privileges):
    columns = columns[:]
    column_restrictions = {}
    for priv in privileges:
        priv_table = priv[0].split('.')[0]
        priv_column = priv[0].split('.')[1]
        priv_scope = priv[1]
        priv_selects = priv[2]
        if priv_table == table.__name__ and priv_column in columns and priv_scope == 'R':
            if priv_column not in column_restrictions:
                column_restrictions[priv_column] = []
            if priv_selects != ():
                column_restrictions[priv_column] = column_restrictions[priv_column].append(priv_selects)
    for column in columns:
        if column in column_restrictions and len(column_restrictions[column]) == 0:
            columns.remove(column)
    return len(columns) == 0


def check_read_on_columns(table, columns, privileges):
    columns = columns[:]
    import sys
    #print >>sys.stderr, columns
    for priv in privileges:
        priv_table = priv[0].split('.')[0]
        priv_column = priv[0].split('.')[1]
        priv_scope = priv[1]
        priv_selects = priv[2]
        #print >>sys.stderr, priv_table, priv_column, priv_scope, str(table.__name__)
        if priv_table == table.__name__ and priv_column in columns and priv_scope == 'R':
            columns.remove(priv_column)

    #print >>sys.stderr, columns
    return len(columns) == 0


def append_weak_read_filter_by_conditions(table, columns, privileges, filter_by):
    for priv in privileges:
        priv_table = priv[0].split('.')[0]
        priv_column = priv[0].split('.')[1]
        priv_scope = priv[1]
        priv_selects = priv[2]
        if priv_table == table.__name__ and priv_column in columns and priv_scope == 'R' and priv_selects != ():
            filter_by &= simql.query_handler.compile_filter_by(table, priv_selects)
   # print >>sys.stderr, filter_by
    return filter_by

