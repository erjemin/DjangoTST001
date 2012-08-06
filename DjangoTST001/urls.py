# -*- coding: utf-8 -*-
# Включили поддержку UTF-8 в Python. Без этого даже комментарии на русском языке нельзя писать.

from django.conf.urls import *
# from django.conf.urls import patterns, include, url

from DjangoTST001.views import hello
from DjangoTST001.views import funMainHomePage
from DjangoTST001.views import hours_ahead
from DjangoTST001.views import junk_nav

# Расскоментить следующие две строки для активации интерфейса администратора
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    ( r'^hello/$', hello ),
    ( r'^time/$', funMainHomePage ),
    ( r'^time/plus/(\d{1,2})/$', hours_ahead ),
    ( r'^nav/(\d{1,6})/$', junk_nav ),
    # Пример:
    # url(r'^$', 'DjangoTST001.views.home', name='home'),
    # url(r'^DjangoTST001/', include('DjangoTST001.foo.urls')),

    # Раскоментить строку admin/doc ниже для активации документации по администрированию:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Расскоментить следующую строку для активации интерфейса администратора:
    url(r'^admin/', include(admin.site.urls)),
)
