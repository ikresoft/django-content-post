from django import template
from content_post import get_post_model
from content.models import Category
from categories.views import get_category_for_path

register = template.Library()


class PostByCategoryNode(template.Node):

    def __init__(self, category, template):
        self.category = category
        self.template = template

    def render(self, context):
        t = template.loader.get_template(self.template)
        if isinstance(self.category, basestring):
            try:
                self.category = get_category_for_path(self.category, queryset=Category.objects.all())
                posts = get_post_model().published.filter(categories=self.category)
                context['posts'] = posts
            except:
                pass
        return t.render(context)


def posts_by_category(parser, token):
    template_name = "content_post/templatetags/posts_by_category.html"
    try:
        tag_name, category, template_name = token.split_contents()
        if not (template_name[0] == template_name[-1] and template_name[0] in ('"', "'")):
            raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    except:
        try:
            tag_name, category = token.split_contents()
        except:
            raise template.TemplateSyntaxError("%r tag requires a category argument" % token.contents.split()[0])
    category = category[1:-1]
    template_name = template_name[1:-1]
    return PostByCategoryNode(category, template_name)

register.tag('posts_by_category', posts_by_category)


class PostsByCategoryNode(template.Node):

    def __init__(self, category, limit, var_name, random=False):
        self.var_name = var_name
        self.category = category
        self.limit = limit
        self.random = random

    def render(self, context):
        if self.category is None:
            context[self.var_name] = None
            return ''
        try:
            query = get_post_model().site_objects.filter(feed__category=self.category)
            if self.random is True:
                query = query.order_by('?')

            if self.limit == -1:
                context[self.var_name] = query.all()
            else:
                context[self.var_name] = query.all()[:self.limit]

            if self.limit == 1:
                context[self.var_name] = context[self.var_name][0]

        except:
            context[self.var_name] = None
        return ''


@register.tag()
def get_posts_by_category(parser, token):
    try:
        tag_name, category, limit, random, _as, var_name = token.split_contents()
    except:
        raise TemplateSyntaxError("get_content_by_category tag takes exactly four arguments")
    if (category[0] == category[-1] and category[0] in ('"', "'")):
        try:
            category = get_category_for_path(category[1:-1], queryset=Category.objects.all())
        except:
            category = None
    else:
        category = template.Variable(category)
    limit = int(limit)
    return PostsByCategoryNode(category, limit, var_name, random)


class LatestPosts(template.Node):

    def __init__(self, limit, category_list, var_name):
        self.var_name = var_name
        self.category_list = category_list
        self.limit = int(limit)

    def render(self, context):

        try:
            query = get_post_model().published.order_by("-date_modified")
        except:
            query = get_post_model().published.order_by("-date_created")

        if self.category_list is not None and self.category_list != []:
            if isinstance(self.category_list[0], template.Variable):
                self.category_list = [self.category_list[0].resolve(context)]
            query = query.filter(categories__in=self.category_list)

        if self.limit == -1:
            context[self.var_name] = query.all()
        else:
            context[self.var_name] = query.all()[:self.limit]

        if self.limit == 1:
            context[self.var_name] = context[self.var_name][0]

        return ''


@register.tag()
def get_latest_posts(parser, token):
    try:
        tag_name, limit, category, _as, var_name = token.split_contents()
    except:
        raise TemplateSyntaxError("get_latest_posts tag takes exactly three arguments")

    category_list = []
    if category != '':
        if (category[0] == category[-1] and category[0] in ('"', "'")):
            try:
                cats = [x.strip() for x in category[1:-1].split(',')]
                for cat in cats:
                    category_list.append(get_category_for_path(cat, queryset=Category.objects.all()))
            except:
                pass
        else:
            category_list.append(template.Variable(category))

    return LatestPosts(limit, category_list, var_name)


class PopularPosts(template.Node):

    def __init__(self, limit, category, var_name):
        self.var_name = var_name
        self.category = category
        self.limit = int(limit)

    def render(self, context):
        from datetime import timedelta, date
        enddate = date.today()
        startdate = enddate - timedelta(days=1)
        query = get_post_model().with_counter.filter(date_modified__range=[startdate, enddate])
        if not query:
            startdate = enddate - timedelta(days=2)
            query = get_post_model().with_counter.filter(date_modified__range=[startdate, enddate])

        if self.category is not None:
            self.category = self.category.resolve(context)
            query = query.filter(categories=self.category)

        if self.limit == -1:
            context[self.var_name] = query.all()
        else:
            context[self.var_name] = query.all()[:self.limit]

        return ''


@register.tag()
def get_popular_posts(parser, token):
    try:
        tag_name, limit, category, _as, var_name = token.split_contents()
    except:
        raise TemplateSyntaxError("get_popular_posts tag takes exactly three arguments")

    if category != '':
        if (category[0] == category[-1] and category[0] in ('"', "'")):
            try:
                category = get_category_for_path(category[1:-1], queryset=Category.objects.all())
            except:
                category = None
        else:
            category = template.Variable(category)

    return PopularPosts(limit, category, var_name)


@register.filter
def youtube_url(value):
    from urlparse import urlparse, parse_qs
    try:
        return 'http://www.youtube.com/embed/%s?feature=oembed' % parse_qs(urlparse(value).query)["v"][0]
    except:
        return ''
