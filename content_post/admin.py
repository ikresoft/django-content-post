#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.conf import settings as site_settings
from django.utils.translation import ugettext_lazy as _

from content import settings
from category_content.admin import CategoryContentAdmin
from content_post import get_post_model

class PostAdmin(CategoryContentAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'body')
        }),
        ('Categories', {
            'fields': ('categories',),
        }),
        (_('Post data'), {
            'fields': ('authors', 'non_staff_author',
                       'status', 'origin', 'allow_comments', 'allow_pings', 'is_sticky')
        }),)

    fieldsets = fieldsets + ((_('Advanced Options'), {
            'fields': ('slug', 'date_modified', 'site', ),
            'classes': ('collapse',),
        }),)

admin.site.register(get_post_model(), PostAdmin)
