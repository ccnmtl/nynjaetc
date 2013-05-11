# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'SectionPreferences'
        db.delete_table('main_sectionpreferences')

        # Adding model 'SectionPreference'
        db.create_table('main_sectionpreference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pagetree.Section'])),
            ('preference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Preference'])),
        ))
        db.send_create_signal('main', ['SectionPreference'])

        # Adding unique constraint on 'SectionPreference', fields ['section', 'preference']
        db.create_unique('main_sectionpreference', ['section_id', 'preference_id'])

        # Adding model 'Preference'
        db.create_table('main_preference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('main', ['Preference'])

        # Adding field 'SectionTimestamp.section'
        db.add_column('main_sectiontimestamp', 'section',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['pagetree.Section']),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'SectionPreference', fields ['section', 'preference']
        db.delete_unique('main_sectionpreference', ['section_id', 'preference_id'])

        # Adding model 'SectionPreferences'
        db.create_table('main_sectionpreferences', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('main', ['SectionPreferences'])

        # Deleting model 'SectionPreference'
        db.delete_table('main_sectionpreference')

        # Deleting model 'Preference'
        db.delete_table('main_preference')

        # Deleting field 'SectionTimestamp.section'
        db.delete_column('main_sectiontimestamp', 'section_id')


    models = {
        'main.preference': {
            'Meta': {'object_name': 'Preference'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'main.sectionpreference': {
            'Meta': {'ordering': "['section', 'preference']", 'unique_together': "(('section', 'preference'),)", 'object_name': 'SectionPreference'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Preference']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagetree.Section']"})
        },
        'main.sectiontimestamp': {
            'Meta': {'object_name': 'SectionTimestamp'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagetree.Section']"})
        },
        'pagetree.hierarchy': {
            'Meta': {'object_name': 'Hierarchy'},
            'base_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'pagetree.section': {
            'Meta': {'object_name': 'Section'},
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hierarchy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagetree.Hierarchy']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['main']