from constants import TABLES
import query_handler
from django.db.models import Q
from auth.privilege_validators import check_read_on_columns, append_weak_read_filter_by_conditions, check_strong_read_on_columns


def execute_select(query, privileges):
    if 'from' not in query:
        raise Exception('from required')
    if 'columns' not in query:
        raise Exception('columns required')

    if query['from'] not in TABLES:
        raise Exception('Invalid table ' + query['from'])

    response = None

    table = TABLES[query['from'].lower()]
    columns = query_handler.compile_columns(table, query['columns'])
    if len(set(columns)) != len(columns):
        raise Exception('duplicate columns are not allowed')

    if check_read_on_columns(table, columns, privileges) is False:
        raise Exception('some of the columns are invalid')

    filter_by = Q()
    if 'where' in query and query['where'] is not None:
        filter_by = query_handler.compile_and_permit_filter_by(table, query['where'], privileges)

    filter_by = append_weak_read_filter_by_conditions(table, columns, privileges, filter_by)

    order_by = []
    if 'order_by' in query and query['order_by'] is not None:
        order_by = query_handler.compile_order_by(table, query['order_by'])
    
    if check_strong_read_on_columns(table, [column if column[0] != '-' else column[1:] for column in order_by], privileges) is False:
        raise Exception('some of the columns in order by clause are invalid')

    response = table.objects.filter(filter_by).order_by(*order_by).values(*columns)

    return {'data': [item for item in response]}
