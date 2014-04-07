#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides the Post model for reporting news, events, info etc.
"""
import re

from datetime import datetime

from django.conf import settings as site_settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _
from content import settings
from content.models import Content

class BasePost(Content):
    teaser = models.TextField(_("Teaser Text"), blank=True)
    tease_title = models.CharField(
        _("Tease Headline"),
        max_length=100,
        default="",
        blank=True)
    subhead = models.CharField(
        _("Subheadline"),
        max_length=200,
        blank=True,
        null=True)

    def save(self, *args, **kwargs):
        """
        Enforce setting of publish date and time if it is published.
        """
        if self.status == settings.PUBLISHED_STATUS:
            self.slug = Content.objects.get_unique_slug(self.publish_date, self.slug, self.id)
        super(BasePost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        if self.publish_date is None:
            return ""
        return reverse('post_detail', args=tuple(), kwargs={
            'year': self.publish_date.year,
            'month': self.publish_date.strftime('%b').lower(),
            'day': self.publish_date.day,
            'slug': self.slug
        })

    class Meta(Content.Meta):
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
