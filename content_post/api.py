from rest_framework import serializers, viewsets, filters
from models import *
from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class PostSerializer(serializers.ModelSerializer):
    image_200x150 = serializers.SerializerMethodField('get_image_200x150')
    headline = serializers.CharField(source='headline')
    link_url = serializers.SerializerMethodField('get_link_url')
    categories = CategorySerializer()

    def get_image_200x150(self, obj):
        host = self.context["request"].get_host()
        if obj.image:
            from easy_thumbnails.files import get_thumbnailer
            options = {'size': (200, 150)}
            thumb_url = get_thumbnailer(obj.image).get_thumbnail(options).url
            return 'http://%s%s' % (host, thumb_url)
        return ''

    def get_link_url(self, obj):
        host = self.context["request"].get_host()
        return 'http://%s%s' % (host, obj.get_absolute_url())

    class Meta:
        model = Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = ('id', 'title', 'categories')

    def filter_queryset(self, queryset):
        queryset = super(PostViewSet, self).filter_queryset(queryset)
        limit = self.request.QUERY_PARAMS.get('limit_stop', None)
        if limit:
            return queryset[:limit]
        return queryset
