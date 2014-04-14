from constants import ALLOWED_COLUMNS, TABLES, OP_TO_COLUMN_SUFFIX
from select_query import execute_select
from insert_query import execute_insert
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
        elif query['command'] == 'INSERT':
            results.append(execute_insert(query, privileges))
        else:
            raise Exception('Cannot understand query command ' + query['command'])
    return results


def compile_column(table, column):
    column = column.split(".")[-1].strip('"')

    if column in ALLOWED_COLUMNS[table]:
        return column
    else:
        raise Exception('Invalid column: ' + column)


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
    return [compile_column(table, column) for column in columns]


def compile_and_permit_filter_by(table, where, privileges):
    op = where[0].upper()

    if op in ['AND', 'OR']:
        (left, leftcol) = compile_and_permit_filter_by(table, where[1], privileges)
        (right, rightcol) = compile_and_permit_filter_by(table, where[2], privileges)
        if op == 'AND':
            return left & right, leftcol + rightcol
        elif op == 'OR':
            return left | right, leftcol + rightcol
    elif op in OP_TO_COLUMN_SUFFIX:
        column = compile_column(table, where[1])
        value = where[2]

        if not check_read_on_columns(table, [column], privileges):
            raise Exception('Column ' + column + ' is invalid.')

        if op in ('!=', '<>'):
            return ~Q(**{column: value}), [column]
        else:
            return Q(**{column+OP_TO_COLUMN_SUFFIX[op]: value}), [column]
    else:
        raise Exception('Invalid op')


def compile_filter_by(table, where):
    op = where[0].upper()

    if op in ['AND', 'OR']:
        if op == 'AND':
            return compile_filter_by(table, where[1]) & compile_filter_by(table, where[2])
        elif op == 'OR':
            return compile_filter_by(table, where[1]) | compile_filter_by(table, where[2])
    elif op in OP_TO_COLUMN_SUFFIX:
        column = compile_column(table, where[1])
        value = where[2]

        if op not in ('!=', '<>'):
            return ~Q(**{column: value}), [column]
        else:
            return Q(**{column+OP_TO_COLUMN_SUFFIX[op]: value})
    else:
        raise Exception('Invalid op')


def compile_order_by(table, order_by):
    return ['-' + compile_column(table, column[1:]) if column[0] == '-' else compile_column(table, column) for column in order_by]
