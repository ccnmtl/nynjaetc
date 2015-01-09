# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='encrypted_email',
            field=django_fields.fields.EncryptedEmailField(max_length=485),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='hrsa_id',
            field=django_fields.fields.EncryptedCharField(max_length=485),
            preserve_default=True,
        ),
    ]
