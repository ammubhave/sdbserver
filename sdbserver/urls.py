from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # SimQL
    url(r'^simql/', include('simql.urls')),

    # Admin Site urls
    url(r'^admin/', include(admin.site.urls)),
)