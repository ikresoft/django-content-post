#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL definitions for posts
"""
try:
    from django.conf.urls.defaults import patterns, url
except ImportError:
    from django.conf.urls import patterns, url
from django.views.generic import (ArchiveIndexView, YearArchiveView,
    MonthArchiveView, WeekArchiveView, DayArchiveView, TodayArchiveView,
    DateDetailView)
from models import Post

from views import PathArchiveIndexView

info_dict = {
    'queryset': Post.published.all(),
    'date_field': 'publish_date',
    'allow_empty': True
}

post_info_dict = dict(info_dict.items() + [('template_name', 'content_post/detail.html')])
post_info_dict.pop('allow_empty')

print_info_dict = dict(info_dict.items() + [('template_name', 'content_post/print.html')])
print_info_dict.pop('allow_empty')

urlpatterns = patterns('',

    # news archive index
    url(
        r'^category/(?P<path>.+)/$',
        PathArchiveIndexView.as_view(**info_dict),
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
    # post detail
    url(
        r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        DateDetailView.as_view(**post_info_dict),
        name='post_detail'
    ),
    #story print detail
    url(
        r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/print/$',
        DateDetailView.as_view(**print_info_dict),
        name='post_detail_print',
    ),
)
