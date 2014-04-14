from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^generate_access_token$', 'auth.views.generate_access_token'),
    url(r'^generate_user_access_token$', 'auth.views.generate_user_access_token'),
)