from django.views.generic.dates import YearMixin, MonthMixin, DayMixin, DateMixin, _date_from_string

from django.http import Http404
from django.utils.translation import ugettext as _, get_language
from content.views import CategoryContentListView, CategoryContentDetailView
from content_post import get_post_model
import datetime


class PostListView(CategoryContentListView):
    model = get_post_model()


class PostView(YearMixin, MonthMixin, DayMixin, DateMixin, CategoryContentDetailView):
    model = get_post_model()
    date_field = 'date_modified'
    allow_future = True

    def get_object(self, queryset=None):
        """
        Get the object this request displays.
        """
        year = self.get_year()
        month = self.get_month()
        day = self.get_day()
        date = _date_from_string(year, self.get_year_format(),
                                 month, self.get_month_format(),
                                 day, self.get_day_format())

        # Use a custom queryset if provided
        qs = self.get_queryset() if queryset is None else queryset

        if not self.get_allow_future() and date > datetime.date.today():
            raise Http404(_(
                "Future %(verbose_name_plural)s not available because "
                "%(class_name)s.allow_future is False.") % {
                'verbose_name_plural': qs.model._meta.verbose_name_plural,
                'class_name': self.__class__.__name__,
                },
            )

        # Filter down a queryset from self.queryset using the date from the
        # URL. This'll get passed as the queryset to DetailView.get_object,
        # which'll handle the 404
        lookup_kwargs = self._make_single_date_lookup(date)
        qs = qs.filter(**lookup_kwargs)

        return super(PostView, self).get_object(queryset=qs)
