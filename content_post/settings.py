from django.conf import settings

POST_MODEL = getattr(settings, 'CONTENT_POST_MODEL', 'content_post.Post')
POSTS_PER_PAGE = getattr(settings, 'CONTENT_POSTS_PER_PAGE', 20)
