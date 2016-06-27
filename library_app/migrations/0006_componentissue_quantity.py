# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0005_auto_20160301_0654'),
    ]

    operations = [
        migrations.AddField(
            model_name='componentissue',
            name='quantity',
            field=models.IntegerField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
