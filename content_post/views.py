
from django.views.generic.dates import DateMixin

from category_content.views import CategoryContentListView, CategoryContentDetailView

class PostView(CategoryContentDetailView, DateMixin):
    date_field = 'date_modified'
