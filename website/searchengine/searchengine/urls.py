from django.conf.urls import patterns, include, url

from search.views import *
from indexer.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'searchengine.views.home', name='home'),
    # url(r'^searchengine/', include('searchengine.foo.urls')),

    url(r'^$', home),
    url(r'^index/?$', index),
    url(r'view/([a-zA-z0-9]*.html)$', view_file),
    url(r'index/indexall$', index_all),
    url(r'index/stopwords$',stop_word),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
