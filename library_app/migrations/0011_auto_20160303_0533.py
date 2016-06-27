# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0010_auto_20160303_0524'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reqestissue',
            old_name='user',
            new_name='users',
        ),
    ]
