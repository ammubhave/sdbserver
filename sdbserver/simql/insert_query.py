from constants import TABLES, ALLOWED_COLUMNS
import query_handler
from django.db.models import Q
from auth.privilege_validators import check_read_on_columns, append_weak_read_filter_by_conditions, check_strong_read_on_columns


def execute_insert(query, privileges):
    if 'into' not in query:
        raise Exception('into table required')
    if 'columns' not in query:
        raise Exception('columns required')

    if query['into'] not in TABLES:
        raise Exception('Invalid table ' + query['into'])

    response = None
    #raise Exception(str(query))
    table = TABLES[query['into'].lower()]

    columns = ALLOWED_COLUMNS[table][:]
    for privilege in privileges:
        priv_table = privilege[0].split('.')[0]
        priv_column = privilege[0].split('.')[1]
        priv_mode = privilege[1]
        priv_cond = privilege[2]
        if priv_table == table.__name__ and priv_mode == 'W' and len(priv_cond) == 0 and priv_column in columns:
            columns.remove(priv_column)
    if len(columns) != 0:
        raise Exception('you do not have create privileges for table ' + query['into'])
    
    columns = query_handler.compile_columns(table, query['columns'])
    if len(set(columns)) != len(columns):
        raise Exception('duplicate columns are not allowed')

    columns = query['columns']
    values = query['values']
    create_params = {}
    for index, column in enumerate(columns):
        create_params[column] = values[index]

    response = table(**create_params)
    response.save()
    response = table.objects.filter(id=response.id).values(*ALLOWED_COLUMNS[table])[0]
    #.values(*query['columns'])

    return {'data': {column: response[column] for column in response}}
