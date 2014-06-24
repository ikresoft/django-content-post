#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf import settings as site_settings
from django.utils.translation import ugettext_lazy as _

from content import settings
from category_content.admin import CategoryContentAdmin
from content_post import get_post_model
from forms import PostForm

class PostAdmin(CategoryContentAdmin):
    change_form_template = "admin/content_post/post/change_form.html"
    fieldsets = (
        (None, {
            'fields': (
                ('title', 'slug'),
                'body',
                'tags',)
        }),
        ('Categories', {
            'fields': ('categories',),
        }),
        (_('Post data'), {
            'fields': ('authors', 'non_staff_author',
                       'status', 'origin', 'allow_comments', 'allow_pings', 'is_sticky')
        }),)

    fieldsets = fieldsets + ((_('Advanced Options'), {
            'fields': ('date_modified', 'site', ),
            'classes': ('collapse',),
        }),)

    form = PostForm

admin.site.register(get_post_model(), PostAdmin)
