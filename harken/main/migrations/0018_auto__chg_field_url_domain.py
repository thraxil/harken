# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Url.domain'
        db.alter_column('main_url', 'domain_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['main.Domain']))

    def backwards(self, orm):

        # Changing field 'Url.domain'
        db.alter_column('main_url', 'domain_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Domain'], null=True))

    models = {
        'main.domain': {
            'Meta': {'object_name': 'Domain'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'main.response': {
            'Meta': {'ordering': "['-visited']", 'object_name': 'Response'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'patch': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '200'}),
            'url': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Url']"}),
            'visited': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'main.url': {
            'Meta': {'object_name': 'Url'},
            'content': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Domain']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'db_index': 'True'})
        }
    }

    complete_apps = ['main']