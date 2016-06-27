# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0009_remove_componentissue_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='lend_by',
            field=models.ManyToManyField(default=None, to='library_app.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='componentissue',
            name='quantity',
            field=models.IntegerField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
