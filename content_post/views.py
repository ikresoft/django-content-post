
from django.views.generic.dates import DateMixin

from category_content.views import CategoryContentListView, CategoryContentDetailView


class PostView(DateMixin, CategoryContentDetailView):
    date_field = 'date_modified'
    allow_future = True
