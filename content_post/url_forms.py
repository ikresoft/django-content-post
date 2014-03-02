from django.forms import forms, widgets, fields, models
from django.core import urlresolvers
from django.utils.encoding import force_unicode

from categories.models import Category
from nav_tree import form_registry
from nav_tree.forms import BaseUrlForm


class PostCategoryIndexForm(BaseUrlForm):
    category = models.ModelChoiceField(queryset=Category.objects.all())

    def path(self):
        ancestors = list(self.cleaned_data['category'].get_ancestors()) + [self.cleaned_data['category'], ]
        return '/'.join([force_unicode(i.slug) for i in ancestors])

    def submit(self):
        url = "%s %s" % (self.Meta.url_name, self.path())
        return url

    class Meta:
        verbose_name = 'List by category'
        url_name = 'post_archive_index'

form_registry.register('post_archive_index', PostCategoryIndexForm)
