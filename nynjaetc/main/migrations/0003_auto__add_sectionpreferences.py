# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SectionPreferences'
        db.create_table('main_sectionpreferences', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('main', ['SectionPreferences'])


    def backwards(self, orm):
        # Deleting model 'SectionPreferences'
        db.delete_table('main_sectionpreferences')


    models = {
        'main.sectionpreferences': {
            'Meta': {'object_name': 'SectionPreferences'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'main.sectiontimestamp': {
            'Meta': {'object_name': 'SectionTimestamp'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['main']