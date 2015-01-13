# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('categorycontent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.CategoryContent')),
            ],
            options={
                'abstract': False,
                'swappable': 'CONTENT_POST_MODEL',
            },
            bases=('content.categorycontent',),
        ),
    ]
