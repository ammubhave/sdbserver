from constants import ALLOWED_COLUMNS, TABLES, OP_TO_COLUMN_SUFFIX
from select_query import execute_select
from django.db.models import Q
from auth.privilege_validators import check_read_on_columns


def execute_query(queries, privileges):
    if queries is None:
        raise Exception('queries cannot be None')

    if type(queries) is not list:
        queries = [queries]

    results = []
    for query in queries:
        if 'command' not in query:
            raise Exception('command required')

        if query['command'] == 'SELECT':
            results.append(execute_select(query, privileges))
        else:
            raise Exception('Cannot understand query command ' + query['command'])
    return results


def compile_columns(table, columns):
    """Check for valid column entries and expand if necessary

    If columns is the string '*' then it is expanded into list
    of all allowed columns.

    If columns contains a not-allowed column then raises an
    Exception.

    @param table the table for which the column entries are for
    @param columns the column entries which have to be compiler
    @returns the compiled column list
    @throws Exception if any column in columns is not allowed
    """
    if columns == '*':
        raise Exception("* is not allowed")
        #return ALLOWED_COLUMNS[table]

    compiled_columns = []
    for column in columns:
        column = column.lower()
        if column in ALLOWED_COLUMNS[table]:
            compiled_columns.append(column)
        else:
            raise Exception('Invalid column ' + column)
    return compiled_columns


def compile_and_permit_filter_by(table, where, privileges):
    columns = ALLOWED_COLUMNS[table]

    op = where[0].upper()

    if op in ['AND', 'OR']:
    	(left, leftcol) = compile_and_permit_filter_by(table, where[1], privileges)
    	(right, rightcol) = compile_and_permit_filter_by(table, where[2], privileges)
        if op == 'AND':
            return left & right, leftcol + rightcol
        elif op == 'OR':
            return left | right, leftcol + rightcol
    elif op in OP_TO_COLUMN_SUFFIX:
        column = where[1]
        value = where[2]

        if column not in columns or not check_read_on_columns(table, [column], privileges):
            raise Exception('Column ' + column + ' is invalid.')

        if op == '!=':
            return ~Q(**{column: value}), [column]
        else:
            return Q(**{column+OP_TO_COLUMN_SUFFIX[op]: value}), [column]

    else:
        raise Exception('Invalid op')


def compile_filter_by(table, where):
    columns = ALLOWED_COLUMNS[table]

    op = where[0].upper()

    if op in ['AND', 'OR']:
        if op == 'AND':
            return compile_filter_by(table, where[1]) & compile_filter_by(table, where[2])
        elif op == 'OR':
            return compile_filter_by(table, where[1]) | compile_filter_by(table, where[2])
    elif op in OP_TO_COLUMN_SUFFIX:
        column = where[1]
        value = where[2]

        if column not in columns:
            raise Exception('Column ' + column + ' is invalid.')

        if op == '!=':
            return ~Q(**{column: value}), [column]
        else:
            return Q(**{column+OP_TO_COLUMN_SUFFIX[op]: value})

    else:
        raise Exception('Invalid op')


def compile_order_by(table, order_by):
    columns = ALLOWED_COLUMNS[table]

    for column in order_by:
        if column[0] == '-':
            if column[1:] not in columns:
                raise Exception('Invalid column ' + column[1:])
        else:
            if column not in columns:
                raise Exception('Invalid column ' + column)
    return order_by
