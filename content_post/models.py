#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides the Post model for reporting news, events, info etc.
"""

from django.conf import settings as site_settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from slugify import slugify
from content import settings
from content.models import Content, CategoryContent
from bs4 import BeautifulSoup

VALID_TAGS = ['strong', ]


def sanitize_html(value):

    soup = BeautifulSoup(value)

    for tag in soup.findAll(True):
        if tag.name not in VALID_TAGS:
            tag.hidden = True

    return soup.renderContents()


class BasePost(CategoryContent):

    def get_headline(self):
        try:
            return sanitize_html(self.body[:self.body.index('<!--more--')])
        except:
            return ''
    headline = property(get_headline)

    def save(self, *args, **kwargs):

        super(BasePost, self).save(*args, **kwargs)

    def get_slug(self):
        self.slug = slugify(self.title, ok='-_', only_ascii=True)
        return Content.objects.get_unique_slug(self.date_modified, self.slug, self.id)

    def get_absolute_url(self, category=None, lang=None):
        if category is None:
            category = self.categories.all()[0]
        return reverse('category_post_detail', args=tuple(), kwargs={
            'path': category.slug,
            'year': self.date_modified.year,
            'month': self.date_modified.strftime('%b').lower(),
            'day': self.date_modified.day,
            'slug': self.slug
        })

    class Meta(CategoryContent.Meta):
        abstract = True


class Post(BasePost):

    class Meta(BasePost.Meta):
        swappable = 'CONTENT_POST_MODEL'


# Reversion integration
if settings.USE_REVERSION:
    rev_error_msg = 'Post excepts django-reversion to be '\
                    'installed and in INSTALLED_APPS'
    try:
        import reversion
        if not 'reversion' in site_settings.INSTALLED_APPS:
            raise ImproperlyConfigured(rev_error_msg)
    except (ImportError, ):
        raise ImproperlyConfigured(rev_error_msg)

    reversion.register(Post)
