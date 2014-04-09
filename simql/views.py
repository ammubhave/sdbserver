from django.shortcuts import render
from django.http import HttpResponse
from simql.models import Directory
from simql_to_json_converter import simql_to_json

import json


def compile_columns(table, columns):
    if columns == '*':
        return ALLOWED_COLUMNS[table]

    compiled_columns = []
    for column in columns:
        column = column.lower()
        if column in ALLOWED_COLUMNS[table]:
            compiled_columns.append(column)
        else:
            raise Exception('Invalid column ' + column)
    return compiled_columns


def execute_select(query):
    if 'from' not in query:
        raise Exception('from required')
    if 'columns' not in query:
        raise Exception('columns required')

    if query['from'] not in TABLES:
        raise Exception('Invalid table ' + query['from'])

    response = None

    table = TABLES[query['from'].lower()]
    columns = compile_columns(table, query['columns'])

    response = table.objects.all().values(*columns)

    return {'data': [item for item in response]}


def execute_query(query):

    if query['command'] == 'SELECT':
        return execute_select(query)
    else:
        raise Exception('Cannot understand query command')


def query(request):
    response = {}

    try:
        if 'query' not in request.REQUEST:
            raise Exception('query required')

        if 'type' in request.REQUEST and request.REQUEST['type'] not in ['simql', 'json']:
            raise Exception('type can only be simql or json')

        query = request.REQUEST['query']

        if 'type' in request.REQUEST and request.REQUEST['type'] == 'simql':  # This is a SimQL query
            query = simql_to_json(query)
        else:  # This is a JSON query
            query = json.loads(query)

        response = execute_query(query)
    except Exception as ex:
        return {'error': str(ex)}

    return HttpResponse(json.dumps(response), content_type='application/json')
