# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0012_auto_20160303_0533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentissue',
            name='quantity',
            field=models.IntegerField(default=0, max_length=100),
            preserve_default=True,
        ),
    ]
