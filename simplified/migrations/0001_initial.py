# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Foo'
        db.create_table('simplified_foo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('simplified', ['Foo'])

        # Adding model 'Bar'
        db.create_table('simplified_bar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('foo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['simplified.Foo'])),
            ('barname', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('simplified', ['Bar'])


    def backwards(self, orm):
        # Deleting model 'Foo'
        db.delete_table('simplified_foo')

        # Deleting model 'Bar'
        db.delete_table('simplified_bar')


    models = {
        'simplified.bar': {
            'Meta': {'object_name': 'Bar'},
            'barname': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'foo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['simplified.Foo']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'simplified.foo': {
            'Meta': {'object_name': 'Foo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['simplified']