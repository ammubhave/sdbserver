from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # SimQL
    url(r'^simql/', include('simql.urls')),
    
    # Auth access tokens
    url(r'^auth/', include('auth.urls')),

    url(r'^$', 'auth.views.view_home'),
    url(r'^edit_app', 'auth.views.view_edit_app'),

    # Admin Site urls
    url(r'^admin/', include(admin.site.urls)),
)
