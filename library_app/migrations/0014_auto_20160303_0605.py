# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0013_auto_20160303_0548'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ReturnRequest',
            new_name='RequestReturn',
        ),
    ]
