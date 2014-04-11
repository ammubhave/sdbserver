from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
import json
from auth.models import App, AccessToken, UserPrivilege
from auth.access_token_processor import access_token_generator
from datetime import datetime, timedelta
from django.template import RequestContext


# Should be requested by the app server
def generate_access_token(request):
    response = {}

    try:
        if 'key' not in request.REQUEST or 'secret' not in request.REQUEST:
            raise Exception('key or secret not found')
        app = get_object_or_404(App, app_key=request.REQUEST['key'], app_secret=request.REQUEST['secret'])
        access_token_obj = AccessToken(access_token=access_token_generator(), expires=datetime.now()+timedelta(hours=4), privileges=app.default_privileges)
        access_token_obj.save()
        response['access_token'] = access_token_obj.access_token
    except Exception as ex:
        response['error'] = str(ex)

    return HttpResponse(json.dumps(response), content_type='application/json')

# Should be requested by the user's browser
def generate_user_access_token(request):
    #try:
    if True:
        if 'key' not in request.REQUEST:
            raise Exception('key not found')
        #import os
        #return HttpResponse(str(request))
        app = get_object_or_404(App, app_key=request.REQUEST['key'])
        if request.META['REQUEST_METHOD'] == 'GET':
            user = request.META['SSL_CLIENT_S_DN_Email']
            user = user[:user.index('@')]

            return render_to_response('generate_user_access_token_form.html', {'user': user, 'app_name': 'Directory app'}, RequestContext(request))
        else:
            if 'Login' in request.POST['action']:
                privileges = json.loads(app.default_privileges)
                user = request.META['SSL_CLIENT_S_DN_Email']
                user = user[:user.index('@')]
                user = get_object_or_404(UserPrivilege, user__username=user)

                def combine_app_extended_to_user_privileges(extended_privileges, user_privileges):
                    extended_privileges = [(privilege[0], privilege[1]) for privilege in extended_privileges]
                    privileges = []
                    for privilege in user_privileges:
                        if (privilege[0], privilege[1]) in extended_privileges:
                            privileges.append(privilege)

                    return privileges


                privileges.append(combine_app_extended_to_user_privileges(json.loads(app.extended_privileges), json.loads(user.privileges)))

                access_token_obj = AccessToken(access_token=access_token_generator(), expires=datetime.now()+timedelta(hours=4), privileges=privileges)
                access_token_obj.save()
                return HttpResponseRedirect(app.redirect_url + '?access_token=' + access_token_obj.access_token)
            return HttpResponse('Error: Login rejected')
    #except Exception as ex:
    #    return HttpResponse('Error: ' + str(ex))
