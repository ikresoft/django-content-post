#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from django import forms
from django.utils.translation import ugettext as _

from models import CategoryContent
from content.forms import WIDGET_ATTRS
from category_content.forms import CategoryContentForm

class PostForm(CategoryContentForm):
    subhead = forms.CharField(
        widget=forms.TextInput(attrs=WIDGET_ATTRS),
        max_length=200,
        required=False)
