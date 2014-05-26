#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings as site_settings
from django.utils.translation import ugettext_lazy as _

from content import settings
from content.admin import ChildAdmin
from forms import PostForm
from content_post import get_post_model


class PostAdmin(ChildAdmin):
    base_model = get_post_model()
    fieldsets = (
        (None, {
            'fields': ('title', 'subhead', 'tease_title',
                       'teaser', 'body')
        }),
        ('Categories', {
            'fields': ('categories',),
        }),
        (_('Post data'), {
            'fields': ('authors', 'non_staff_author',
                       'status', 'origin', 'comment_status', )
        }),)

    if settings.INCLUDE_PRINT:
        fieldsets = fieldsets + (_('Print Information'), {
            'fields': ('print_pub_date', 'print_section', 'print_page'),
            'classes': ('collapse',),
        })

    fieldsets = fieldsets + ((_('Advanced Options'), {
            'fields': ('slug', 'date_modified', 'site', ),
            'classes': ('collapse',),
        }),)
    form = PostForm
