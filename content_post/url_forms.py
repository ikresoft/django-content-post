from django.forms import models
from django.utils.encoding import force_unicode

from content.models import Category
from models import Post
from url_browser import form_registry
from url_browser.forms import BaseUrlForm
from content.widgets import MpttTreeWidget
from django_select2 import AutoModelSelect2Field, AutoHeavySelect2Widget


class PostCategoryIndexForm(BaseUrlForm):
    categories = models.ModelMultipleChoiceField(required=True, queryset=Category.objects.all(), widget=MpttTreeWidget)

    def get_path(self):
        paths = []
        for category in self.cleaned_data['categories']:
            ancestors = list(category.get_ancestors()) + [category, ]
            path = '/'.join([force_unicode(i.slug) for i in ancestors])
            paths.append(path)
        return ",".join([path for path in paths])

    def submit(self):
        url = "'%s' '%s'" % (self.Meta.url_name, self.get_path())
        return url

    class Meta:
        verbose_name = 'List by category'
        url_name = 'post_archive_index'

form_registry.register('post_archive_index', PostCategoryIndexForm)


class PostChoicesField(AutoModelSelect2Field):
    queryset = Post.objects
    search_fields = ['title__icontains', "body__icontains"]


class PostDetailForm(BaseUrlForm):
    post = PostChoicesField(widget=AutoHeavySelect2Widget(attrs={"style": "width:400px;"}))

    def submit(self):
        url = "'%s' %d" % (self.Meta.url_name, self.cleaned_data["post"].pk)
        return url

    class Meta:
        verbose_name = 'Choose post'
        url_name = 'category_post_detail'

form_registry.register('category_post_detail', PostDetailForm)
