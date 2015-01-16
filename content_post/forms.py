#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.forms import forms
from django.utils.translation import get_language
from content_post import get_post_model
from content.forms import CategoryContentForm


class PostForm(CategoryContentForm):

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        """The slug + the date_modified must be unique together"""
        if 'date_modified' in cleaned_data and self.instance.pk is None:
            date_modified = cleaned_data['date_modified']
            try:
                get_post_model().objects.get(
                    slug=self.cleaned_data['slug%s' % ('_' + get_language().replace('-', '_'))],
                    date_modified__year=date_modified.year,
                    date_modified__month=date_modified.month,
                    date_modified__day=date_modified.day)
                raise forms.ValidationError(
                    'Please enter a different slug. The one you'\
                    'entered is already being used for {0}'.format(
                         date_modified.strftime("%Y-%b-%d")))
            except get_post_model().DoesNotExist:
                pass
        return cleaned_data

    class Meta:
        model = get_post_model()
        fields = "__all__"
