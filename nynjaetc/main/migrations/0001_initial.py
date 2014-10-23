# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pagetree', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SectionAlternateNavigation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alternate_back', models.CharField(help_text=b'An alternate back button on this section will point to this path.', max_length=64, null=True, blank=True)),
                ('alternate_back_label', models.CharField(help_text=b'A label for this alternate back button, if necessary.', max_length=64, null=True, blank=True)),
                ('alternate_next', models.CharField(help_text=b'An alternate next button on this section will point to this path.', max_length=64, null=True, blank=True)),
                ('alternate_next_label', models.CharField(help_text=b'A label for this alternate next button, if necessary.', max_length=64, null=True, blank=True)),
                ('section', models.ForeignKey(to='pagetree.Section', unique=True)),
            ],
            options={
                'verbose_name': 'Alt. nav setting',
                'verbose_name_plural': 'Alt. nav settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SectionPreference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('preference', models.ForeignKey(to='main.Preference')),
                ('section', models.ForeignKey(to='pagetree.Section')),
            ],
            options={
                'ordering': ['section', 'preference'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SectionQuizAnsweredCorrectly',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('section', models.ForeignKey(to='pagetree.Section')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SectionTimestamp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('section', models.ForeignKey(to='pagetree.Section')),
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
                ('encrypted_email', django_fields.fields.EncryptedEmailField(max_length=229)),
                ('hrsa_id', django_fields.fields.EncryptedCharField(max_length=229)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='sectionpreference',
            unique_together=set([('section', 'preference')]),
        ),
    ]
