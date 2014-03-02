#!/usr/bin/env python

from setuptools import setup, find_packages
github_url = 'https://github.com/ikresoft/django-content-post'


setup(
    name='django-content-post',
    version='1.0',
    description='Django Content Posts',
    long_description='Django Content Posts',
    author='Enver Bisevac, Mirza Delic',
    author_email='ikresoft@gmail.com',
    url=github_url,
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django, Django Content',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False,
)
