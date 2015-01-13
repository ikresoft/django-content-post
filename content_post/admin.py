#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from content.admin import CategoryContentAdmin
from content_post import get_post_model
from forms import PostForm
import translation


class PostAdmin(CategoryContentAdmin):
    change_form_template = "admin/content_post/post/change_form.html"
    fieldsets = (
        (None, {
            'fields':
                ('title', 'slug'),
        }),
        (_('Content'), {
            'fields': ('body',),
            'classes': ('full-width',),
        }),
        ('Categories', {
            'fields': ('categories',),
        }),
        (_('Post data'), {
            'fields': ('tags', 'authors', 'non_staff_author',
                       'status', 'origin', 'allow_comments', 'allow_pings', 'is_sticky')
        }),)

    fieldsets = fieldsets + ((_('Advanced Options'), {
            'fields': ('date_modified', 'site', ),
            'classes': ('collapse',),
        }),)

    form = PostForm

admin.site.register(get_post_model(), PostAdmin)
