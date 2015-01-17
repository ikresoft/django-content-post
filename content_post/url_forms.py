from django.forms import forms, widgets, fields, models
from django.core import urlresolvers
from django.utils.encoding import force_unicode

from categories.models import Category
from url_browser import form_registry
from url_browser.forms import BaseUrlForm


class PostCategoryIndexForm(BaseUrlForm):
    categories = models.ModelMultipleChoiceField(queryset=Category.objects.all())

    def get_path(self):
        paths = []
        for category in self.cleaned_data['categories']:
            ancestors = list(category.get_ancestors()) + [category, ]
            path = '/'.join([force_unicode(i.slug) for i in ancestors])
            paths.append(path)
        return ",".join([path for path in paths])

    def submit(self):
        url = "%s %s" % (self.Meta.url_name, r"'%s'" % self.get_path())
        return url

    class Meta:
        verbose_name = 'List by category'
        url_name = 'post_archive_index'

form_registry.register('post_archive_index', PostCategoryIndexForm)
