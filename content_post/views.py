#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import EmptyPage, InvalidPage
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.encoding import force_unicode
from django.template.loader import find_template
from django.template.base import TemplateDoesNotExist

from django.views.generic import (ArchiveIndexView, YearArchiveView,
    MonthArchiveView, WeekArchiveView, DayArchiveView, TodayArchiveView,
    DateDetailView, ListView, DetailView)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from content import settings
from models import Post

from categories.views import get_category_for_path
from content_post import get_post_model

from settings import POSTS_PER_PAGE


class PostsByCategoryListView(ListView):
    model = get_post_model()
    template_name = "content_post/list.html"

    def get_sub_categories(self, category):
        qs = category.get_descendants()
        categories = [category.pk]
        for node in qs:
            categories.append(node.pk)
        return categories

    def get_context_data(self, **kwargs):
        context = super(PostsByCategoryListView, self).get_context_data(**kwargs)
        try:
            context['category'] = get_category_for_path(self.kwargs["path"])
            self.category = context['category']
        except:
            raise Http404

        posts = self.model.published.filter(categories__in=self.get_sub_categories(context['category'])).order_by('-date_modified')

        paginator = Paginator(posts, POSTS_PER_PAGE)
        page = self.request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        return context

    def get_template_names(self):
        opts = self.model._meta
        app_label = opts.app_label
        ancestors = list(self.category.get_ancestors()) + [self.category, ]
        path = '/'.join([force_unicode(i.slug) for i in ancestors])
        search_templates = [
            "%s/%ss/%s/list.html" % (app_label, opts.object_name.lower(), path),
            "%s/%ss/list.html" % (app_label, opts.object_name.lower()),
            "%s/list.html" % app_label,
            "list.html"
        ]

        for template in search_templates:
            try:
                find_template(template)
                return [template]
            except TemplateDoesNotExist:
                pass
        else:  # pragma: no cover
            pass


class PostDetailView(DetailView):
    model = get_post_model()
    context_object_name = 'post'
    category = None

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        if 'path' in self.kwargs:
            try:
                context['category'] = get_category_for_path(self.kwargs["path"])
                self.category = context['category']
            except:
                raise Http404

        related_posts = self.model.published.filter(
            tags__name__in=list(self.object.tags.values_list('name', flat=True))
        ).exclude(id=self.object.id).distinct().order_by("-date_modified")
        context['related_posts'] = related_posts[:5]
        return context

    def get_template_names(self):
        opts = self.object.get_real_instance()._meta
        app_label = opts.app_label
        ancestors = list(self.category.get_ancestors()) + [self.category, ]
        path = '/'.join([force_unicode(i.slug) for i in ancestors])
        search_templates = [
            "%s/%ss/%s/detail.html" % (app_label, opts.object_name.lower(), path),
            "%s/%ss/detail.html" % (app_label, opts.object_name.lower()),
            "%s/detail.html" % app_label,
            "detail.html"
        ]

        for template in search_templates:
            try:
                find_template(template)
                return [template]
            except TemplateDoesNotExist:
                pass
        else:  # pragma: no cover
            pass


class LatestPostsListView(ListView):

    model = get_post_model()
    template_name = 'content_post/list.html'

    def get_context_data(self, **kwargs):
        context = super(LatestPostsListView, self).get_context_data(**kwargs)
        try:
            posts = self.model.published.order_by("-date_modified")
        except:
            posts = self.model.published.order_by("-date_created")

        paginator = Paginator(posts, POSTS_PER_PAGE)
        page = self.request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        return context
