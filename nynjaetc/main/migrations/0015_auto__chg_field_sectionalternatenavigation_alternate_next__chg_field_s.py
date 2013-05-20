# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        from south.db import engine
        # Renaming column for 'SectionAlternateNavigation.alternate_next' to match new field type.
        db.rename_column('main_sectionalternatenavigation', 'alternate_next_id', 'alternate_next')
        # Changing field 'SectionAlternateNavigation.alternate_next'
        db.alter_column('main_sectionalternatenavigation', 'alternate_next', self.gf('django.db.models.fields.CharField')(max_length=512, null=True))
        # Removing index on 'SectionAlternateNavigation', fields ['alternate_next']
        if 'sqlite' not in engine:
            db.delete_index('main_sectionalternatenavigation', ['alternate_next_id'])


        # Renaming column for 'SectionAlternateNavigation.alternate_back' to match new field type.
        db.rename_column('main_sectionalternatenavigation', 'alternate_back_id', 'alternate_back')
        # Changing field 'SectionAlternateNavigation.alternate_back'
        db.alter_column('main_sectionalternatenavigation', 'alternate_back', self.gf('django.db.models.fields.CharField')(max_length=512, null=True))
        # Removing index on 'SectionAlternateNavigation', fields ['alternate_back']
        if 'sqlite' not in engine:
            db.delete_index('main_sectionalternatenavigation', ['alternate_back_id'])


    def backwards(self, orm):
        # Adding index on 'SectionAlternateNavigation', fields ['alternate_back']
        db.create_index('main_sectionalternatenavigation', ['alternate_back_id'])

        # Adding index on 'SectionAlternateNavigation', fields ['alternate_next']
        db.create_index('main_sectionalternatenavigation', ['alternate_next_id'])


        # Renaming column for 'SectionAlternateNavigation.alternate_next' to match new field type.
        db.rename_column('main_sectionalternatenavigation', 'alternate_next', 'alternate_next_id')
        # Changing field 'SectionAlternateNavigation.alternate_next'
        db.alter_column('main_sectionalternatenavigation', 'alternate_next_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['pagetree.Section']))

        # Renaming column for 'SectionAlternateNavigation.alternate_back' to match new field type.
        db.rename_column('main_sectionalternatenavigation', 'alternate_back', 'alternate_back_id')
        # Changing field 'SectionAlternateNavigation.alternate_back'
        db.alter_column('main_sectionalternatenavigation', 'alternate_back_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['pagetree.Section']))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.preference': {
            'Meta': {'object_name': 'Preference'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'main.sectionalternatenavigation': {
            'Meta': {'object_name': 'SectionAlternateNavigation'},
            'alternate_back': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'alternate_next': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagetree.Section']", 'unique': 'True'})
        },
        'main.sectionpreference': {
            'Meta': {'ordering': "['section', 'preference']", 'unique_together': "(('section', 'preference'),)", 'object_name': 'SectionPreference'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Preference']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagetree.Section']"})
        },
        'main.sectionquizansweredcorrectly': {
            'Meta': {'object_name': 'SectionQuizAnsweredCorrectly'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagetree.Section']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'main.sectiontimestamp': {
            'Meta': {'object_name': 'SectionTimestamp'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagetree.Section']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'main.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'encrypted_email': ('django_fields.fields.EncryptedEmailField', [], {'max_length': '101', 'cipher': "'AES'"}),
            'hrsa_id': ('django_fields.fields.EncryptedCharField', [], {'max_length': '101', 'cipher': "'AES'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
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
