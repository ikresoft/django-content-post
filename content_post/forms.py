#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from django import forms
from django.utils.translation import ugettext as _

from models import Post
from content.forms import ContentForm, SlugMixin, WIDGET_ATTRS

class PostForm(ContentForm, SlugMixin):
    subhead = forms.CharField(
        widget=forms.TextInput(attrs=WIDGET_ATTRS),
        max_length=200,
        required=False)
