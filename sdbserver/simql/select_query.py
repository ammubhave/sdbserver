from constants import TABLES
import query_handler
from django.db.models import Q
from auth.privilege_validators import check_read_on_columns, append_weak_read_filter_by_conditions, check_strong_read_on_columns


def execute_select(query, privileges):
    # Check FROM
    assert 'from' in query
    query['from'] = query['from'].strip('"')
    if query['from'] not in TABLES:
        raise Exception('Invalid table: ' + query['from'])

    table = TABLES[query['from']]

    # Check select_columns
    assert 'columns' in query
    columns = query_handler.compile_columns(table, query['columns'])
    if len(set(columns)) != len(columns):
        raise Exception('Duplicate columns not allowed')

    if check_read_on_columns(table, columns, privileges) is False:
        raise Exception('Some of the columns are privileged')

    # Where
    filter_by, filter_by_columns = Q(), []
    if 'where' in query and query['where'] is not None:
        filter_by, filter_by_columns = query_handler.compile_and_permit_filter_by(table, query['where'], privileges)
    #raise Exception(filter_by_columns)

    filter_by = append_weak_read_filter_by_conditions(table, list(set(columns+filter_by_columns)), privileges, filter_by)

    order_by = []
    if 'order_by' in query:
        order_by = query_handler.compile_order_by(table, query['order_by'])

    if check_strong_read_on_columns(table, [column if column[0] != '-' else column[1:] for column in order_by], privileges) is False:
        raise Exception('Some of the columns in order by clause are privileged')

    response = table.objects.filter(filter_by).order_by(*order_by).values_list(*columns)
    #return {'data': [item for item in response]}
    return [item for item in response]
