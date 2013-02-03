# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Response.url'
        db.delete_column('main_response', 'url')


        # Changing field 'Response.orig_url'
        db.alter_column('main_response', 'orig_url_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['main.Url']))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Response.url'
        raise RuntimeError("Cannot reverse this migration. 'Response.url' and its values cannot be restored.")

        # Changing field 'Response.orig_url'
        db.alter_column('main_response', 'orig_url_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Url'], null=True))

    models = {
        'main.response': {
            'Meta': {'ordering': "['-visited']", 'object_name': 'Response'},
            'body': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'orig_url': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Url']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '200'}),
            'visited': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'main.url': {
            'Meta': {'object_name': 'Url'},
            'content': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'db_index': 'True'})
        }
    }

    complete_apps = ['main']
