# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
import diff_match_patch

def get_patch(url, content=""):
    """ return a text patch of the supplied content against
    existing content """
    dmp = diff_match_patch.diff_match_patch()
    return dmp.patch_toText(dmp.patch_make(url.content, content))


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        for r in orm['main.Response'].objects.all():
            r.patch = get_patch(r.url, r.body)
            r.save()

    def backwards(self, orm):
        "Write your backwards methods here."
        pass

    models = {
        'main.response': {
            'Meta': {'ordering': "['-visited']", 'object_name': 'Response'},
            'body': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'db_index': 'True'})
        }
    }

    complete_apps = ['main']
    symmetrical = True
