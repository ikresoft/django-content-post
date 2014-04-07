from django.conf import settings

POST_MODEL = getattr(settings, 'CONTENT_POST_MODEL', 'content_post.Post')
