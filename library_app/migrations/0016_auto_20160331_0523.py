# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0015_auto_20160331_0505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='lend_by',
            field=models.ManyToManyField(default=None, to='library_app.UserProfile', null=True, blank=True),
            preserve_default=True,
        ),
    ]
