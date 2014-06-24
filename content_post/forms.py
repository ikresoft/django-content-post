#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from django.forms import fields, widgets, forms
from django.utils.translation import ugettext as _

from content_post import get_post_model
from content.forms import WIDGET_ATTRS
from category_content.forms import CategoryContentForm

class PostForm(CategoryContentForm):

	class Meta:
		model = get_post_model()
