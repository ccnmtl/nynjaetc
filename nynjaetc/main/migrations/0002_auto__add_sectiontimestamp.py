# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SectionTimestamp'
        db.create_table('main_sectiontimestamp', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('main', ['SectionTimestamp'])


    def backwards(self, orm):
        # Deleting model 'SectionTimestamp'
        db.delete_table('main_sectiontimestamp')


    models = {
        'main.sectiontimestamp': {
            'Meta': {'object_name': 'SectionTimestamp'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['main']