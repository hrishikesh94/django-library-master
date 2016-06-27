# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('lend_from', models.DateField(null=True, blank=True)),
                ('total', models.IntegerField(max_length=100)),
                ('issued', models.IntegerField(default=0, null=True, blank=True)),
                ('remaining', models.IntegerField(default=0, null=True, blank=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LendPeriods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('days_amount', models.IntegerField()),
            ],
            options={
                'ordering': ['days_amount'],
                'get_latest_by': 'days_amount',
                'verbose_name': 'Lending period',
                'verbose_name_plural': 'Lending periods',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
                'get_latest_by': 'name',
                'verbose_name': 'Catagory',
                'verbose_name_plural': 'Catagories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReqestIssue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.TimeField(default=django.utils.timezone.now)),
                ('status', models.BooleanField(default=1)),
                ('component', models.ForeignKey(to='library_app.Component')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mobile', models.CharField(max_length=15, null=True, blank=True)),
                ('website', models.CharField(max_length=50, null=True, blank=True)),
                ('fb_name', models.CharField(max_length=60, null=True, blank=True)),
                ('join_date', models.DateField()),
                ('friends', models.ManyToManyField(related_name='friends_rel_+', to='library_app.UserProfile')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
                'get_latest_by': 'join_date',
                'verbose_name': 'User profile',
                'verbose_name_plural': 'User profiles',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='component',
            name='catagory',
            field=models.ForeignKey(to='library_app.Publisher'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='component',
            name='lend_by',
            field=models.ManyToManyField(to='library_app.UserProfile', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='component',
            name='lend_period',
            field=models.ForeignKey(to='library_app.LendPeriods'),
            preserve_default=True,
        ),
    ]
