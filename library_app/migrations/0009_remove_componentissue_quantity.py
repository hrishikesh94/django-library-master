# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0008_remove_component_lend_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='componentissue',
            name='quantity',
        ),
    ]
