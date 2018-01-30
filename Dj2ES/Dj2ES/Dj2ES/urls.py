"""
Definition of urls for Dj2ES.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    
    url(r'^$', app.views.home, name='home'),
    url(r'^datasets', app.views.datasets, name='datasets'),
    url(r'^contact', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^search', app.views.search, name='search'),
    url(r'^view', app.views.view, name='view'),
    url(r'^simple_upload', app.views.simple_upload, name='simple_upload'),
    url(r'^fs_upload', app.views.fs_upload, name='fs_upload'),
    url(r'^conf_id', app.views.conf_id, name='conf_id'),

    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
