from django import template
from django.template import RequestContext
from django.template.loader import render_to_string
from content_post.models import Post
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
                self.category = get_category_for_path(self.category)
                posts = Post.published.filter(categories=self.category)
                context['posts'] = posts
            except:
                pass
        return t.render(context)

def posts_by_category(parser, token):
    template_name="content_post/templatetags/posts_by_category.html"
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
