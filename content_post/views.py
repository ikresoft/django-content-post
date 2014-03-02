#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import EmptyPage, InvalidPage
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.views.generic import (ArchiveIndexView, YearArchiveView,
    MonthArchiveView, WeekArchiveView, DayArchiveView, TodayArchiveView,
    DateDetailView)

from content import settings
from models import Post

from categories.views import get_category_for_path


class PathArchiveIndexView(ArchiveIndexView):

    def get_dated_queryset(self, ordering=None, **lookup):
        category = get_category_for_path(self.kwargs['path'])
        qs = super(PathArchiveIndexView, self).get_dated_queryset(ordering, **lookup)
        return qs.filter(categories=category)


