# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BadCodeWarning'
        db.create_table('questions_badcodewarning', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.Question'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('warn_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('code', self.gf('django.db.models.fields.TextField')()),
            ('error_type', self.gf('django.db.models.fields.IntegerField')()),
            ('admin_comment', self.gf('django.db.models.fields.CharField')(blank=True, null=True, max_length=240)),
        ))
        db.send_create_signal('questions', ['BadCodeWarning'])

        # Deleting field 'Validated.failed_message'
        db.delete_column('questions_validated', 'failed_message')


    def backwards(self, orm):
        # Deleting model 'BadCodeWarning'
        db.delete_table('questions_badcodewarning')

        # Adding field 'Validated.failed_message'
        db.add_column('questions_validated', 'failed_message',
                      self.gf('django.db.models.fields.TextField')(blank=True, null=True),
                      keep_default=False)


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'questions.answerchoice': {
            'Meta': {'object_name': 'AnswerChoice'},
            'choice_expr': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'choice_text': ('django.db.models.fields.CharField', [], {'default': "'${choice_expr}$'", 'max_length': '240'}),
            'choice_type': ('django.db.models.fields.CharField', [], {'default': "'DIST'", 'max_length': '20'}),
            'comment': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '240'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"})
        },
        'questions.badcodewarning': {
            'Meta': {'object_name': 'BadCodeWarning'},
            'admin_comment': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '240'}),
            'code': ('django.db.models.fields.TextField', [], {}),
            'error_type': ('django.db.models.fields.IntegerField', [], {}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'warn_datetime': ('django.db.models.fields.DateTimeField', [], {})
        },
        'questions.blockrecipe': {
            'Meta': {'object_name': 'BlockRecipe'},
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.DocumentRecipe']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_columns': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'num_exercises': ('django.db.models.fields.IntegerField', [], {}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"}),
            'space_after': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'questions.condition': {
            'Meta': {'object_name': 'Condition'},
            'condition_text': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"})
        },
        'questions.document': {
            'Meta': {'object_name': 'Document'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.DocumentRecipe']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'questions.documentrecipe': {
            'Meta': {'object_name': 'DocumentRecipe'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'questions.exercise': {
            'Meta': {'object_name': 'Exercise'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"}),
            'vardict': ('picklefield.fields.PickledObjectField', [], {})
        },
        'questions.question': {
            'Meta': {'object_name': 'Question'},
            'body': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'code': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'date_added': ('django.db.models.fields.DateField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '240'}),
            'prompt': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '240'}),
            'symbol_vars': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '240'})
        },
        'questions.randvar': {
            'Meta': {'object_name': 'RandVar'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"}),
            'varname': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'varposs': ('django.db.models.fields.CharField', [], {'max_length': '240'})
        },
        'questions.validated': {
            'Meta': {'object_name': 'Validated'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_verified': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'num_poss': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['questions.Question']"}),
            'validated_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'vardicts': ('picklefield.fields.PickledObjectField', [], {'null': 'True'})
        }
    }

    complete_apps = ['questions']