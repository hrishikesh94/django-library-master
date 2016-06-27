# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0004_auto_20160301_0526'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComponentIssue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.TimeField(default=django.utils.timezone.now)),
                ('component', models.ForeignKey(to='library_app.Component')),
                ('user', models.ForeignKey(to='library_app.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='reqestissue',
            name='status',
        ),
        migrations.AlterField(
            model_name='component',
            name='lend_by',
            field=models.ManyToManyField(default=None, to='library_app.UserProfile'),
            preserve_default=True,
        ),
    ]
