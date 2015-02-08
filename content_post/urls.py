#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL definitions for posts
"""
try:
    from django.conf.urls.defaults import patterns, url
except ImportError:
    from django.conf.urls import patterns, url
from django.views.generic import (
    YearArchiveView, MonthArchiveView, WeekArchiveView, DayArchiveView, TodayArchiveView
)
from content_post import get_post_model
from views import *

from rest_framework.routers import DefaultRouter
from api import PostViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'post', PostViewSet)

info_dict = {
    'queryset': get_post_model().published.all(),
    'date_field': 'date_',
    'allow_empty': True
}

urlpatterns = patterns('',
    # post detail
    url(
        r'^category/(?P<path>.+)/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        PostView.as_view(),
        name='category_post_detail'
    ),

    # news archive index
    url(
        r'^category/(?P<path>.+)/$',
        PostListView.as_view(),
        name='post_archive_index'
    ),
    # news archive year list
    url(
        r'^category/(?P<path>.+)/(?P<year>\d{4})/$',
        YearArchiveView.as_view(**info_dict),
        name='post_archive_year'
    ),
    # news archive month list
    url(
        r'^category/(?P<path>.+)/(?P<year>\d{4})/(?P<month>\w{3})/$',
        MonthArchiveView.as_view(**info_dict),
        name='post_archive_month'
    ),
    # news archive week list
    url(
        r'^category/(?P<path>.+)/(?P<year>\d{4})/(?P<week>\d{1,2})/$',
        WeekArchiveView.as_view(**info_dict),
        name='post_archive_week'
    ),
    # news archive day list
    url(
        r'^category/(?P<path>.+)/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
        DayArchiveView.as_view(**info_dict),
        name='post_archive_day'
    ),
    # news archive today list
    url(
        r'^category/(?P<path>.+)/today/$',
        TodayArchiveView.as_view(**info_dict),
        name='post_archive_day'
    ),
)
