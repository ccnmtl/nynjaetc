# flake8: noqa
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GenotypeActivityBlock'
        db.create_table(u'treatment_activity_genotypeactivityblock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'treatment_activity', ['GenotypeActivityBlock'])


    def backwards(self, orm):
        # Deleting model 'GenotypeActivityBlock'
        db.delete_table(u'treatment_activity_genotypeactivityblock')


    models = {
        u'treatment_activity.genotypeactivityblock': {
            'Meta': {'object_name': 'GenotypeActivityBlock'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'treatment_activity.treatmentactivityblock': {
            'Meta': {'object_name': 'TreatmentActivityBlock'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'treatment_activity.treatmentnode': {
            'Meta': {'object_name': 'TreatmentNode'},
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'help': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'treatment_activity.treatmentpath': {
            'Meta': {'object_name': 'TreatmentPath'},
            'cirrhosis': ('django.db.models.fields.BooleanField', [], {}),
            'drug_choice': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'treatment_status': ('django.db.models.fields.IntegerField', [], {}),
            'tree': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['treatment_activity.TreatmentNode']"})
        }
    }

    complete_apps = ['treatment_activity']