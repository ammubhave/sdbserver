from django.shortcuts import render
from django.http import HttpResponse
from simql.models import Directory
from simql_to_json_converter import simql_to_json
import json
from query_handler import execute_query
from auth.constants import PUBLIC_ACCESS_TOKEN
from auth.access_token_processor import access_token_to_privileges


def query(request):
    response = {}

    #try:
    if True:
        if 'query' not in request.REQUEST:
            raise Exception('query required')

        access_token = PUBLIC_ACCESS_TOKEN
        if 'access_token' in request.REQUEST:
            access_token = request.REQUEST['access_token']

        if 'type' in request.REQUEST and request.REQUEST['type'] not in ['simql', 'json']:
            raise Exception('type can only be simql or json')

        query = request.REQUEST['query']

        if 'type' in request.REQUEST and request.REQUEST['type'] == 'simql':  # This is a SimQL query
            #query = simql_to_json(query)
            query = json.loads(query)
        else:  # This is a JSON query
            query = simql_to_json(query)
            if query is None:
                raise Exception('malformed SimQL query')
            #query = json.loads(query)
        #return HttpResponse(str(query))

        privileges = access_token_to_privileges(access_token)

        response = execute_query(query, privileges)
   # except Exception as ex:
       # response = {'error': str(ex)}
       # raise ex

    return HttpResponse(json.dumps(response), content_type='application/json')
