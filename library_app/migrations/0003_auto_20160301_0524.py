# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0002_auto_20160229_0642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='lend_by',
            field=models.ManyToManyField(default=None, to=settings.AUTH_USER_MODEL, null=True, blank=True),
            preserve_default=True,
        ),
    ]
