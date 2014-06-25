
from django.views.generic.dates import DateMixin

from category_content.views import CategoryContentListView, CategoryContentDetailView
from content_post import get_post_model

class PostListView(CategoryContentListView):
    model = get_post_model()

class PostView(DateMixin, CategoryContentDetailView):
    model = get_post_model()
    date_field = 'date_modified'
    allow_future = True

    def dispatch(self, request, *args, **kwargs):
        return super(PostView, self).dispatch(request, *args, **kwargs)
