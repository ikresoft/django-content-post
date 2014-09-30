from rest_framework import serializers, viewsets
from models import *


class PostSerializer(serializers.ModelSerializer):
    image_200x150 = serializers.SerializerMethodField('get_image_200x150')
    headline = serializers.CharField('headline')
    link_url = serializers.SerializerMethodField('get_link_url')

    def get_image_200x150(self, obj):
        host = self.context["request"].get_host()
        if obj.image:
            from easy_thumbnails.files import get_thumbnailer
            options = {'size': (200, 150)}
            thumb_url = get_thumbnailer(obj.image).get_thumbnail(options).url
            return 'http://%s%s' % (host, thumb_url)
        return ''

    def get_link_url(self, obj):
        return ''

    class Meta:
        model = Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
