# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0007_returnrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='component',
            name='lend_by',
        ),
    ]
