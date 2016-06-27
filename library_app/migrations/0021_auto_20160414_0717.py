# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0020_auto_20160414_0716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='lend_period',
            field=models.ForeignKey(to='library_app.LendPeriods'),
            preserve_default=True,
        ),
    ]
