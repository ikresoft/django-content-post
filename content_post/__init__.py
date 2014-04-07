"""
An application for handling posts on a web site
"""

__version_info__ = {
    'major': 1,
    'minor': 0,
    'micro': 0,
    'releaselevel': 'alpha',
    'serial': 1
}


def get_version(short=False):
    assert __version_info__['releaselevel'] in ('alpha', 'beta', 'final')
    vers = ["%(major)i.%(minor)i" % __version_info__, ]
    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final' and not short:
        vers.append('%s%i' % (__version_info__['releaselevel'][0], __version_info__['serial']))
    return ''.join(vers)

__version__ = get_version()

from content_post import settings

def get_post_model():
    """
    Returns the User model that is active in this project.
    """
    from django.db.models import get_model

    try:
        app_label, model_name = settings.POST_MODEL.split('.')
    except ValueError:
        raise ImproperlyConfigured("CONTENT_POST_MODEL must be of the form 'app_label.model_name'")
    user_model = get_model(app_label, model_name)
    if user_model is None:
        raise ImproperlyConfigured("CONTENT_POST_MODEL refers to model '%s' that has not been installed" % settings.POST_MODEL)
    return user_model
